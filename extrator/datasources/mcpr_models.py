from sqlalchemy import (
    MetaData,
    Table,
    Column,
    NUMERIC,
    String)

# meta = MetaData(schema='mcpr')
meta = MetaData()

TB_DOCUMENTO = Table(
    'mcpr_documento',
    meta,
    Column(
        'docu_dk',
        NUMERIC(
            precision=12,
            scale=0,
            asdecimal=False),
        primary_key=True,
        nullable=False),
    Column('docu_nr_externo', String(length=20)),
    Column('docu_mate_dk', NUMERIC(precision=4, scale=0, asdecimal=False))
)
