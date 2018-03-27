from ..base.utils import conn, logger, session
from .tjrj_models import TB_PROCESSO, TB_MOVIMENTO_PROCESSO
from .mcpr_models import TB_DOCUMENTO
from sqlalchemy.sql.expression import func


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


def obter_por_numero_processo(numero):
    return session().query(
        TB_PROCESSO).where(
            TB_PROCESSO.c.numero_processo == numero).first()


@transacao
def insere_documento(documento):
    # TODO: somente insert falso por enquanto
    insert = _preenche_valores(documento, TB_PROCESSO.insert())
    conn().execute(insert)


def atualizar_documento(documento):
    insert = _preenche_valores(
        documento,
        TB_PROCESSO.update().where(
            id=documento.id))
    conn().execute(insert)

    movimentos_inserir = _itens_não_presentes(insert['id'], documento['itens'])

    for movimento in movimentos_inserir:
        insere_movimento(insert['id'], movimento)


def insere_movimento(id_documento, movimento):
    trans = conn().begin()
    try:
        pass
        trans.transaction.commit()
    except Exception as error:
        logger().error(error)
        trans.transaction.rollback()


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