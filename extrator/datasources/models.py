from ..base.utils import conn, logger, session
from .tjrj_models import (
    TB_PROCESSO,
    TB_MOVIMENTO_PROCESSO,
    TB_ITEM_MOVIMENTO,
    SQ_ITEM_MOVIMENTO,
    SQ_MOVIMENTO,
    # SQ_PROCESSO
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
    return wrapper


def _preenche_valores(documento, tabela):
    tabela.values(
        executado='',
        advogado_s='adevogado',
        numero_do_tombo='',
        oficio_de_registro='',
        folha='',
        requerido='',
        exequente='',
        representante_legal='',
        acao='',
        comunicante='',
        requerente='',
        bairro='',
        livro='',
        pai='',
        mae='',
        aviso_ao_advogado='',
        status='',
        comarca='',
        assistente='',
        cidade='',
        autor_do_fato='',
        acusado='',
        impetrado='',
        impetrante='',
        notificado='',
        autor='',
        intimado='',
        idoso='',
        avo_avo='',
        numero_processo='',
        reu='',
        reclamado='',
        endereco='',
        prazo='',
        classe='',
        assunto=''
    )
    return tabela


def obter_documentos_externos():
    query = session().query(
        TB_DOCUMENTO.c.docu_nr_externo,
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


def obter_por_numero_processo(numero_documento):
    return session().query(
        TB_PROCESSO).where(
            TB_PROCESSO.c.numero_processo == numero_documento).first()


def insere_movimento(dk_processo, movimento):
    id_inserido = _insere_movimento(dk_processo, movimento)

    for item in movimento:
        if item in ['hash', 'tipo-do-movimento']:
            continue
        _insere_item_movimento(id_inserido, item, movimento[item])

    return id_inserido


def _insere_movimento(dk_processo, movimento):
    insert = TB_MOVIMENTO_PROCESSO.insert().values(
        prmv_dk=SQ_MOVIMENTO.next_value(),
        prmv_prtj_dk=dk_processo,
        prmv_tp_movimento=movimento['tipo-do-movimento'],
        prmv_dt_ultima_atualizacao=sysdate(),
        prmv_hash=movimento['hash']
    )
    if 'inteiro-teor' in movimento:
        insert.values(prmv_tx_inteiro_teor=movimento['inteiro-teor'])

    resultado = conn().execute(insert)
    return resultado.inserted_primary_key[0]


@transacao
def _insere_item_movimento(dk_movimento, chave, valor):
    insert = TB_ITEM_MOVIMENTO.insert().values(
        mvit_dk=SQ_ITEM_MOVIMENTO.next_value(),
        mvit_prmv_dk=dk_movimento,
        mvit_tp_chave=chave,
        mvit_tp_valor=valor
    )
    conn().execute(insert)


@transacao
def _insere_documento(documento):
    # TODO: somente insert falso por enquanto
    insert = _preenche_valores(documento, TB_PROCESSO.insert())
    conn().execute(insert)


@transacao
def _atualizar_documento(documento):
    insert = _preenche_valores(
        documento,
        TB_PROCESSO.update().where(
            id=documento.id))
    conn().execute(insert)

# movimentos_inserir = _itens_não_presentes(insert['id'], documento['itens'])


def _itens_não_presentes(movimentos, lista_hashs):
    retorno = []
    for movimento in movimentos:
        if movimento['hash'] not in lista_hashs:
            retorno += [movimento]

    return retorno


def obtem_hashs_movimentos(id_documento):
    return [doc[0] for doc in TB_MOVIMENTO_PROCESSO.select(
        'hash').where(
            id_documento=id_documento)]
