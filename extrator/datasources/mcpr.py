from ..base.utils import conn, logger
from .mcpr_models import TB_DOCUMENTO

SELECT_DOCU_EXTERNO = """
    select docu_nr_externo as DOCU_NR_EXTERNO
      from mcpr.mcpr_documento
     where
        docu_mate_dk = 4 and
        length(docu_nr_externo) = 20"""


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
    return [doc[0] for doc in conn().execute(SELECT_DOCU_EXTERNO)]


@transacao
def insere_documento(documento):
    # TODO: somente insert falso por enquanto
    insert = _preenche_valores(documento, TB_DOCUMENTO.insert())
    conn().execute(insert)


def atualizar_documento(documento):
    insert = _preenche_valores(
        documento,
        TB_DOCUMENTO.update().where(
            id=documento.id))
    conn().execute(insert)


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
