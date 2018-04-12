import os
import cx_Oracle
from sqlalchemy import create_engine
from extrator.settings import DS_EXADATA_CONN_CSTR
from extrator.base.utils import engine, set_log, engine_cx
from extrator.datasources.models import (
    obter_documentos_externos,
    atualizar_documento,
    atualizar_vista)
from extrator.crawler.pipeliner import pipeline
from extrator.settings import (
    DS_EXADATA_HOST,
    DS_EXADATA_PORT,
    DS_EXADATA_SID,
    DS_EXADATA_user,
    DS_EXADATA_password,
    INSTANCIAS)
from multiprocessing.dummy import Pool
from newrelic.agent import background_task

PARALELO = True


def main():
    os.environ['NLS_LANG'] = 'American_America.UTF8'
    engine['connection'] = create_engine(
        DS_EXADATA_CONN_CSTR,
        convert_unicode=False,
        pool_recycle=10,
        pool_size=50,
        # echo=True,
        encoding="utf-8"
    )

    dsn_tns = cx_Oracle.makedsn(
        DS_EXADATA_HOST, DS_EXADATA_PORT, DS_EXADATA_SID)
    engine_cx['connection'] = cx_Oracle.connect(
        DS_EXADATA_user,
        DS_EXADATA_password,
        dsn_tns,
        encoding="UTF-8",
        nencoding="UTF-8",
        threaded=True)
    engine_cx['connection'].autocommit = True

    set_log()

    docs = obter_documentos_externos()

    if PARALELO:
        pool = Pool(INSTANCIAS)

        return pool.map(processar_armazenar, docs[:10000])
    else:
        retorno = []
        for item in map(processar_armazenar, docs[:10000]):
            retorno += [item]
        return retorno


def processar_armazenar(doc):

    retorno = None

    @background_task()
    def wrapper(doc):
        global retorno
        try:
            documento = pipeline(doc[0])
            if documento == {}:
                atualizar_vista(doc[0], doc[1])
                raise Exception("Documento %s não encontrado no TJRJ" % doc[0])
            atualizar_documento(documento, doc[1])
            retorno = "Atualizado: %s" % str(doc[0])
        except Exception as error:
            atualizar_vista(doc[0], doc[1])
            retorno = "Problema: doc %s - %s" % (str(doc), str(error))
            raise error

    try:
        wrapper(doc)
    except Exception:
        pass

    return retorno


if __name__ == '__main__':
    main()
