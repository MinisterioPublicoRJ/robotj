import json
import cx_Oracle
from ..base.utils import conn, session, cxoracle
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
        return funcao(*args, **kwargs)
        # trans = conn().begin()
        # try:
        #     retorno = funcao(*args, **kwargs)
        #     trans.transaction.commit()
        #     return retorno
        # except Exception as error:
        #     logger().error(error)
        #     trans.transaction.rollback()
        #     raise error
    return wrapper


def obtem(documento, chave):
    return json.dumps(documento.get(chave))


def _preenche_valores(documento, tabela):
    tabela = tabela.values(
        prtj_cd_numero_processo=documento.get('numero-processo'),
        prtj_tx_executado=obtem(documento, 'executado'),
        prtj_tx_advogado_s=obtem(documento, 'advovado-s'),
        prtj_tx_numero_do_tombo=obtem(documento, 'numero-do-tombo'),
        prtj_tx_oficio_de_registro=obtem(documento, 'oficio-de-registro'),
        prtj_tx_folha=obtem(documento, 'folha'),
        prtj_tx_requerido=obtem(documento, 'requerido'),
        prtj_tx_exequente=obtem(documento, 'exequente'),
        prtj_tx_representante_legal=obtem(documento, 'representante-legal'),
        prtj_tx_acao=obtem(documento, 'acao'),
        prtj_tx_comunicante=obtem(documento, 'comunicante'),
        prtj_tx_requerente=obtem(documento, 'requerente'),
        prtj_tx_bairro=obtem(documento, 'bairro'),
        prtj_tx_livro=obtem(documento, 'livro'),
        prtj_tx_pai=obtem(documento, 'pai'),
        prtj_tx_mae=obtem(documento, 'mae'),
        prtj_tx_aviso_ao_advogado=obtem(documento, 'aviso-ao-advogado'),
        prtj_tx_status=obtem(documento, 'status'),
        prtj_tx_comarca=obtem(documento, 'comarca'),
        prtj_tx_assistente=obtem(documento, 'assistente'),
        prtj_tx_cidade=obtem(documento, 'cidade'),
        prtj_tx_autor_do_fato=obtem(documento, 'autor-do-fato'),
        prtj_tx_acusado=obtem(documento, 'acusado'),
        prtj_tx_impetrado=obtem(documento, 'impetrado'),
        prtj_tx_impetrante=obtem(documento, 'impetrante'),
        prtj_tx_notificado=obtem(documento, 'notificado'),
        prtj_tx_autor=obtem(documento, 'autor'),
        prtj_tx_intimado=obtem(documento, 'intimado'),
        prtj_tx_idoso=obtem(documento, 'idoso'),
        prtj_tx_avo_avo=obtem(documento, 'avo-avo'),
        prtj_tx_reu=obtem(documento, 'reu'),
        prtj_tx_reclamado=obtem(documento, 'reclamado'),
        prtj_tx_endereco=obtem(documento, 'endereco'),
        prtj_tx_prazo=obtem(documento, 'prazo'),
        prtj_tx_classe=obtem(documento, 'classe'),
        prtj_tx_assunto=obtem(documento, 'assunto'),
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
    retorno = session().query(
        TB_PROCESSO.c.prtj_dk,
        TB_PROCESSO.c.prtj_hash
        ).filter(
            TB_PROCESSO.c.prtj_cd_numero_processo == numero_documento
        ).first()

    return retorno


# ------------------------------------------------------------------------
# Atualizacao de Movimento
# ------------------------------------------------------------------------


def _insere_item_movimento_db(dk_movimento, chave, valor):
    insert = TB_ITEM_MOVIMENTO.insert().values(
        mvit_dk=SQ_ITEM_MOVIMENTO.next_value(),
        mvit_prmv_dk=dk_movimento,
        mvit_tp_chave=chave,
        mvit_tp_valor=json.dumps(valor)
    )
    conn().execute(insert)


def _insere_movimento_blob_db(dk_processo, movimento):
    sql = ("INSERT INTO SYSTEM.TJRJ_PROCESSO_MOVIMENTO_TJ "
           "(PRMV_DK, PRMV_PRTJ_DK, PRMV_TP_MOVIMENTO, "
           "PRMV_DT_ULTIMA_ATUALIZACAO, PRMV_TX_INTEIRO_TEOR, PRMV_HASH) "
           "VALUES(SEQ_TJRJ_PROCESSO_MOVIMENTO_TJ.NEXTVAL, :DK_PROCESSO, "
           ":TP_MOVIMENTO, SYSDATE, :PRMV_TX_INTEIRO_TEOR,:HASH) "
           "returning PRMV_DK into :x")

    cursor = cxoracle().cursor()
    seq = cursor.var(cx_Oracle.NUMBER)
    cursor.setinputsizes(PRMV_TX_INTEIRO_TEOR=cx_Oracle.BLOB)
    cursor.prepare(
        sql
    )

    cursor.execute(
        None,
        DK_PROCESSO=dk_processo,
        TP_MOVIMENTO=movimento['tipo-do-movimento'],
        PRMV_TX_INTEIRO_TEOR=movimento['inteiro-teor'].encode('utf-8'),
        HASH=movimento['hash'],
        x=seq)

    cursor.close()

    return seq.getvalue()


def _insere_movimento_db(dk_processo, movimento):
    if 'inteiro-teor' in movimento:
        return _insere_movimento_blob_db(dk_processo, movimento)

    insert = TB_MOVIMENTO_PROCESSO.insert().values(
        prmv_dk=SQ_MOVIMENTO.next_value(),
        prmv_prtj_dk=dk_processo,
        prmv_tp_movimento=movimento['tipo-do-movimento'],
        prmv_dt_ultima_atualizacao=sysdate(),
        prmv_hash=movimento['hash']
    )

    resultado = conn().execute(insert)
    return resultado.inserted_primary_key[0]


def insere_movimento(dk_processo, movimento):
    id_inserido = _insere_movimento_db(dk_processo, movimento)

    for item in movimento:
        if item in ['hash', 'tipo-do-movimento', 'inteiro-teor']:
            continue
        _insere_item_movimento_db(id_inserido, item, movimento[item])

    return id_inserido

# ------------------------------------------------------------------------
# Atualizacao de Documento
# ------------------------------------------------------------------------


def atualizar_documento(documento, docu_dk):
    processo = _obter_por_numero_processo(documento['numero-processo'])

    if processo:
        if processo[1] == documento['hash']:
            atualizar_vista(documento['numero-processo'], docu_dk, processo)
            return

        id_processo = processo[0]
        _atualizar_documento_db(documento, id_processo)
    else:
        id_processo = _insere_documento_db(documento, docu_dk)

    hashs_existentes = _obtem_hashs_movimentos(id_processo)
    movimentos_inserir = _itens_não_presentes(
        documento['itens'],
        hashs_existentes)

    for movimento in movimentos_inserir:
        insere_movimento(id_processo, movimento)


def atualizar_vista(numero_documento, docu_dk, processo=None):
    processo = processo if processo else _obter_por_numero_processo(
        numero_documento)

    if processo:
        _atualiza_vista_db(processo[0])
    else:
        _insere_vista_db(numero_documento, docu_dk)


def _insere_vista_db(numero_documento, docu_dk):
    insert = TB_PROCESSO.insert().values(
        prtj_dk=SQ_PROCESSO.next_value(),
        prtj_docu_dk=docu_dk,
        prtj_cd_numero_processo=numero_documento,
        prtj_dt_ultima_atualizacao=sysdate(),
        prtj_dt_ultima_vista=sysdate(),
    )

    conn().execute(insert)


def _atualiza_vista_db(id_processo):
    update = TB_PROCESSO.update().where(
        TB_PROCESSO.c.prtj_dk == id_processo
    ).values(
        prtj_dt_ultima_vista=sysdate()
    )

    conn().execute(update)


def _insere_documento_db(documento, docu_dk):
    insert = TB_PROCESSO.insert()

    insert = _preenche_valores(documento, insert)

    insert = insert.values(
        prtj_docu_dk=docu_dk,
        prtj_dk=SQ_PROCESSO.next_value(),
    )

    resultado = conn().execute(insert)

    return resultado.inserted_primary_key[0]


def _atualizar_documento_db(documento, prtj_dk):
    update = TB_PROCESSO.update()

    update = _preenche_valores(documento, update)

    update = update.where(
        TB_PROCESSO.c.prtj_dk == prtj_dk
    )

    conn().execute(update)


def _itens_não_presentes(movimentos, lista_hashs):
    retorno = []
    for movimento in movimentos:
        if movimento['hash'] not in lista_hashs:
            retorno += [movimento]

    return retorno


def _obtem_hashs_movimentos(prtj_dk):
    return [doc[0] for doc in session().query(
        TB_MOVIMENTO_PROCESSO.c.prmv_hash).filter(
        TB_MOVIMENTO_PROCESSO.c.prmv_prtj_dk == prtj_dk
    )]
