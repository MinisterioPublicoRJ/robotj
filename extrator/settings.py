import os
import cx_Oracle


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
