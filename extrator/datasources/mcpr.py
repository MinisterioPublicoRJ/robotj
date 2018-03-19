from extrator.settings import conn

SELECT_DOCU_EXTERNO = """
    select docu_nr_externo as DOCU_NR_EXTERNO
      from mcpr.mcpr_documento
     where
        docu_mate_dk = 4 and
        length(docu_nr_externo) = 20"""


def obter_documentos_externos():
    return conn().execute(SELECT_DOCU_EXTERNO)
