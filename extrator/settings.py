import os
import cx_Oracle
import logging

POOLCOUNT=50

DS_EXADATA_HOST=os.environ['DB_HOST']
DS_EXADATA_PORT=1521
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