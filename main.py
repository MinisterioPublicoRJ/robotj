from sqlalchemy import create_engine
from extrator.settings import DS_EXADATA_CONN_CSTR
from extrator.base.utils import engine, set_log
from extrator.datasources.mcpr import obter_documentos_externos
from extrator.crawler.pipeliner import pipeline


def main():
    engine['connection'] = create_engine(
        DS_EXADATA_CONN_CSTR,
        convert_unicode=False,
        pool_recycle=10,
        pool_size=50,
        echo=True
    )

    set_log()

    docs = obter_documentos_externos()

    for item in pipeline(docs):
        pass


if __name__ == '__main__':
    main()
