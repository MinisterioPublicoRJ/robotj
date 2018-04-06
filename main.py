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
    DS_EXADATA_password)
# from multiprocessing import Pool


def main():
    engine['connection'] = create_engine(
        DS_EXADATA_CONN_CSTR,
        convert_unicode=False,
        pool_recycle=10,
        pool_size=50,
        echo=True
    )

    dsn_tns = cx_Oracle.makedsn(
        DS_EXADATA_HOST, DS_EXADATA_PORT, DS_EXADATA_SID)
    engine_cx['connection'] = cx_Oracle.connect(
        DS_EXADATA_user, DS_EXADATA_password, dsn_tns)
    engine_cx['connection'].autocommit = True

    set_log()

    docs = obter_documentos_externos()

    for doc in docs:
        try:
            documento = pipeline(doc[0])
            if documento == {}:
                continue
            atualizar_documento(documento, doc[1])
        except Exception as error:
            atualizar_vista(doc[0], doc[1])

    # pool = Pool(POOLCOUNT)

    # resultados = pool.map(processar_armazenar, docs[0:1000])

    # print(resultados)


def processar_armazenar(documento):
    try:
        pipeline(documento)
    except Exception as ex:
        return {'documento': documento, 'resultado': ex}
    # aqui armazena no banco e blah
    return {'documento': documento, 'resultado': 'Yay'}


if __name__ == '__main__':
    main()
