import os
import cx_Oracle
import logging
import newrelic.agent

POOLCOUNT=50

NEW_RELIC_ENVIRONMENT = os.environ.get("NEW_RELIC_ENVIRONMENT")

INSTANCIAS = int(os.environ.get("INSTANCIAS", 2))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DS_EXADATA_HOST=os.environ['DB_HOST']
DS_EXADATA_PORT=os.environ['DB_PORT']
DS_EXADATA_SID=os.environ['DB_SID']
DS_EXADATA_user=os.environ['DB_USER']
DS_EXADATA_password=os.environ['DB_PASSWORD']

DS_EXADATA_CONN_SID = cx_Oracle.makedsn(
    DS_EXADATA_HOST,
    DS_EXADATA_PORT,
    sid=DS_EXADATA_SID)

DS_EXADATA_CONN_CSTR = 'oracle://{user}:{password}@{sid}'.format(
    user=DS_EXADATA_user,
    password=DS_EXADATA_password,
    sid=DS_EXADATA_CONN_SID
)

LOGGER_FORMAT = '%(asctime)-15s %(message)s'
LOGGER_LEVEL = logging.INFO

URL_PROCESSO = ("http://www4.tjrj.jus.br/consultaProcessoWebV2/"
                "consultaMov.do?v=2&numProcesso={doc_number}&"
                "acessoIP=internet&tipoUsuario")
