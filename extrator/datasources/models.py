from ..base.utils import conn, logger, session
from .tjrj_models import (
    TB_PROCESSO,
    TB_MOVIMENTO_PROCESSO,
    TB_ITEM_MOVIMENTO,
    SQ_ITEM_MOVIMENTO,
    SQ_MOVIMENTO,
    SQ_PROCESSO
)
from .mcpr_models import TB_DOCUMENTO
from sqlalchemy.sql.expression import func
from sqlalchemy.sql.functions import sysdate


def transacao(funcao):
    def wrapper(*args, **kwargs):
        trans = conn().begin()
        try:
            retorno = funcao(*args, **kwargs)
            trans.transaction.commit()
            return retorno
        except Exception as error:
            logger().error(error)
            trans.transaction.rollback()
            raise error
    return wrapper


def _preenche_valores(documento, tabela):
    tabela = tabela.values(
        prtj_cd_numero_processo=documento.get('numero-processo'),
        prtj_tx_executado=documento.get('executado'),
        prtj_tx_advogado_s=documento.get('advovado-s'),
        prtj_tx_numero_do_tombo=documento.get('numero-do-tombo'),
        prtj_tx_oficio_de_registro=documento.get('oficio-de-registro'),
        prtj_tx_folha=documento.get('folha'),
        prtj_tx_requerido=documento.get('requerido'),
        prtj_tx_exequente=documento.get('exequente'),
        prtj_tx_representante_legal=documento.get('representante-legal'),
        prtj_tx_acao=documento.get('acao'),
        prtj_tx_comunicante=documento.get('comunicante'),
        prtj_tx_requerente=documento.get('requerente'),
        prtj_tx_bairro=documento.get('bairro'),
        prtj_tx_livro=documento.get('livro'),
        prtj_tx_pai=documento.get('pai'),
        prtj_tx_mae=documento.get('mae'),
        prtj_tx_aviso_ao_advogado=documento.get('aviso-ao-advogado'),
        prtj_tx_status=documento.get('status'),
        prtj_tx_comarca=documento.get('comarca'),
        prtj_tx_assistente=documento.get('assistente'),
        prtj_tx_cidade=documento.get('cidade'),
        prtj_tx_autor_do_fato=documento.get('autor-do-fato'),
        prtj_tx_acusado=documento.get('acusado'),
        prtj_tx_impetrado=documento.get('impetrado'),
        prtj_tx_impetrante=documento.get('impetrante'),
        prtj_tx_notificado=documento.get('notificado'),
        prtj_tx_autor=documento.get('autor'),
        prtj_tx_intimado=documento.get('intimado'),
        prtj_tx_idoso=documento.get('idoso'),
        prtj_tx_avo_avo=documento.get('avo-avo'),
        prtj_tx_reu=documento.get('reu'),
        prtj_tx_reclamado=documento.get('reclamado'),
        prtj_tx_endereco=documento.get('endereco'),
        prtj_tx_prazo=documento.get('prazo'),
        prtj_tx_classe=documento.get('classe'),
        prtj_tx_assunto=documento.get('assunto'),
        prtj_dt_ultima_atualizacao=sysdate(),
        prtj_dt_ultima_vista=sysdate(),
        prtj_hash=documento.get('hash'),
    )
    return tabela


def obter_documentos_externos():
    query = session().query(
        TB_DOCUMENTO.c.docu_nr_externo,
        TB_DOCUMENTO.c.docu_dk,
        TB_PROCESSO.c.prtj_dt_ultima_vista).outerjoin(
        TB_PROCESSO,
        TB_DOCUMENTO.c.docu_nr_externo == TB_PROCESSO.c.prtj_cd_numero_processo
    ).filter(
        TB_DOCUMENTO.c.docu_mate_dk == 4
    ).filter(
            func.length(TB_DOCUMENTO.c.docu_nr_externo) == 20).order_by(
        TB_PROCESSO.c.prtj_dt_ultima_vista
    )
    return [(doc[0], doc[1]) for doc in query]


def _obter_por_numero_processo(numero_documento):
    return session().query(
        TB_PROCESSO).filter(
            TB_PROCESSO.c.prtj_cd_numero_processo == numero_documento
        ).first()


# ------------------------------------------------------------------------
# Atualizacao de Movimento
# ------------------------------------------------------------------------


@transacao
def _insere_item_movimento_db(dk_movimento, chave, valor):
    insert = TB_ITEM_MOVIMENTO.insert().values(
        mvit_dk=SQ_ITEM_MOVIMENTO.next_value(),
        mvit_prmv_dk=dk_movimento,
        mvit_tp_chave=chave,
        mvit_tp_valor=valor
    )
    conn().execute(insert)


@transacao
def _insere_movimento_db(dk_processo, movimento):
    insert = TB_MOVIMENTO_PROCESSO.insert().values(
        prmv_dk=SQ_MOVIMENTO.next_value(),
        prmv_prtj_dk=dk_processo,
        prmv_tp_movimento=movimento['tipo-do-movimento'],
        prmv_dt_ultima_atualizacao=sysdate(),
        prmv_hash=movimento['hash']
    )
    if 'inteiro-teor' in movimento:
        insert = insert.values(prmv_tx_inteiro_teor=movimento['inteiro-teor'])

    resultado = conn().execute(insert)
    return resultado.inserted_primary_key[0]


@transacao
def insere_movimento(dk_processo, movimento):
    id_inserido = _insere_movimento_db(dk_processo, movimento)

    for item in movimento:
        if item in ['hash', 'tipo-do-movimento']:
            continue
        _insere_item_movimento_db(id_inserido, item, movimento[item])

    return id_inserido

# ------------------------------------------------------------------------
# Atualizacao de Documento
# ------------------------------------------------------------------------


@transacao
def atualizar_documento(documento, docu_dk):
    processo = _obter_por_numero_processo(documento['numero-processo'])

    if processo:
        if processo['prtj_hash'] == documento['hash']:
            atualizar_vista(documento['numero-processo'], docu_dk, processo)
            return

        id_processo = processo['prtj_dk']
        _atualizar_documento_db(documento, id_processo)
    else:
        id_processo = _insere_documento_db(documento, docu_dk)

    hashs_existentes = _obtem_hashs_movimentos(id_processo)
    movimentos_inserir = _itens_não_presentes(
        documento['itens'],
        hashs_existentes)

    for movimento in movimentos_inserir:
        insere_movimento(id_processo, movimento)


@transacao
def atualizar_vista(numero_documento, docu_dk, processo=None):
    processo = processo if processo else _obter_por_numero_processo(
        numero_documento)

    if processo:
        _atualiza_vista_db(processo['prtj_dk'])
    else:
        _insere_vista_db(numero_documento, docu_dk)


@transacao
def _insere_vista_db(numero_documento, docu_dk):
    insert = TB_PROCESSO.insert().values(
        prtj_dk=SQ_PROCESSO.next_value(),
        prtj_docu_dk=docu_dk,
        prtj_cd_numero_processo=numero_documento,
        prtj_dt_ultima_atualizacao=sysdate(),
        prtj_dt_ultima_vista=sysdate(),
    )

    conn().execute(insert)


@transacao
def _atualiza_vista_db(id_processo):
    update = TB_PROCESSO.update().where(
        TB_PROCESSO.c.prtj_dk == id_processo
    ).values(
        prtj_dt_ultima_vista=sysdate()
    )

    conn().execute(update)


@transacao
def _insere_documento_db(documento, docu_dk):
    insert = TB_PROCESSO.insert()

    insert = _preenche_valores(documento, insert)

    insert = insert.values(
        prtj_docu_dk=docu_dk,
        prtj_dk=SQ_PROCESSO.next_value(),
    )

    resultado = conn().execute(insert)

    return resultado.inserted_primary_key[0]


@transacao
def _atualizar_documento_db(documento, prtj_dk):
    insert = TB_PROCESSO.update()

    insert = _preenche_valores(documento, insert)

    insert = insert.values(
        prtj_dk=SQ_PROCESSO.next_value(),
    ).where(
        prtj_dk=prtj_dk
    )

    conn().execute(insert)


def _itens_não_presentes(movimentos, lista_hashs):
    retorno = []
    for movimento in movimentos:
        if movimento['hash'] not in lista_hashs:
            retorno += [movimento]

    return retorno


def _obtem_hashs_movimentos(prtj_dk):
    return [doc[0] for doc in conn().execute(
        TB_MOVIMENTO_PROCESSO.select(
            'hash').where(
                prmv_prtj_dk=prtj_dk))]
