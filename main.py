from sqlalchemy import create_engine
from extrator.settings import DS_EXADATA_CONN_CSTR, engine
from extrator.datasources.mcpr import obter_documentos_externos
from extrator.crawler.parser import parse_metadados

def main():
    engine['connection'] = create_engine(
        DS_EXADATA_CONN_CSTR,
        convert_unicode=False,
        pool_recycle=10,
        pool_size=50,
        echo=True
    )

    return obter_documentos_externos()


if __name__ == '__main__':
    main()
