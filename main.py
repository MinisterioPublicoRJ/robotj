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
    NEWRELIC_APPLICATION)
from multiprocessing.dummy import Pool
from newrelic.agent import record_custom_event


POOLCOUNT = 30

PARALELO = False


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
        pool = Pool(POOLCOUNT)

        return pool.map(processar_armazenar, docs)
    else:
        retorno = []
        for item in map(processar_armazenar, docs):
            retorno += [item]
        return retorno


def processar_armazenar(doc):
    try:
        documento = pipeline(doc[0])
        if documento == {}:
            return
        atualizar_documento(documento, doc[1])
        print("Atualizado: %s" % str(doc[0]))
        record_custom_event('info', {
            'acao': 'atualizar_documento',
            'documento': doc[0]},
            application=NEWRELIC_APPLICATION)
        return "Atualizado: %s" % str(doc[0])
    except Exception as error:
        print("Problema: doc %s - %s" % (str(doc), str(error)))
        record_custom_event('error', {
            'acao': 'atualizar_documento',
            'documento': doc[0],
            'mensagem': error},
            application=NEWRELIC_APPLICATION)
        atualizar_vista(doc[0], doc[1])
        return "Problema: doc %s - %s" % (str(doc), str(error))


if __name__ == '__main__':
    main()
