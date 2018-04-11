from sqlalchemy import (
    MetaData,
    Table,
    Sequence,
    Column,
    Integer,
    String,
    DateTime,
    LargeBinary)

# meta = MetaData(schema='tjrj')
meta = MetaData()

SQ_PROCESSO = Sequence('SEQ_TJRJ_PROCESSO_TJ')
SQ_MOVIMENTO = Sequence('SEQ_TJRJ_PROCESSO_MOVIMENTO_TJ')
SQ_ITEM_MOVIMENTO = Sequence('SEQ_TJRJ_MOVIMENTO_ITEM_TJ')

TB_PROCESSO = Table(
    'tjrj_processo_tj',
    meta,
    Column('prtj_dk', Integer(), primary_key=True),
    Column('prtj_docu_dk', Integer()),
    Column('prtj_cd_numero_processo', String(25)),
    Column('prtj_tx_executado', String(400)),
    Column('prtj_tx_advogado_s', String(400)),
    Column('prtj_tx_numero_do_tombo', String(400)),
    Column('prtj_tx_oficio_de_registro', String(400)),
    Column('prtj_tx_folha', String(400)),
    Column('prtj_tx_requerido', String(400)),
    Column('prtj_tx_exequente', String(400)),
    Column('prtj_tx_representante_legal', String(400)),
    Column('prtj_tx_acao', String(400)),
    Column('prtj_tx_comunicante', String(400)),
    Column('prtj_tx_requerente', String(400)),
    Column('prtj_tx_bairro', String(400)),
    Column('prtj_tx_livro', String(400)),
    Column('prtj_tx_pai', String(400)),
    Column('prtj_tx_mae', String(400)),
    Column('prtj_tx_aviso_ao_advogado', String(400)),
    Column('prtj_tx_status', String(400)),
    Column('prtj_tx_comarca', String(400)),
    Column('prtj_tx_assistente', String(400)),
    Column('prtj_tx_cidade', String(400)),
    Column('prtj_tx_autor_do_fato', String(400)),
    Column('prtj_tx_acusado', String(400)),
    Column('prtj_tx_impetrado', String(400)),
    Column('prtj_tx_impetrante', String(400)),
    Column('prtj_tx_notificado', String(400)),
    Column('prtj_tx_autor', String(400)),
    Column('prtj_tx_intimado', String(400)),
    Column('prtj_tx_idoso', String(400)),
    Column('prtj_tx_avo_avo', String(400)),
    Column('prtj_tx_reu', String(400)),
    Column('prtj_tx_reclamado', String(400)),
    Column('prtj_tx_endereco', String(400)),
    Column('prtj_tx_prazo', String(400)),
    Column('prtj_tx_classe', String(400)),
    Column('prtj_tx_assunto', String(400)),
    Column('prtj_dt_ultima_atualizacao', DateTime()),
    Column('prtj_dt_ultima_vista', DateTime()),
    Column('prtj_hash', String(32))
)


TB_MOVIMENTO_PROCESSO = Table(
    'tjrj_processo_movimento_tj',
    meta,
    Column('prmv_dk', Integer, primary_key=True),
    Column('prmv_prtj_dk', Integer()),
    Column('prmv_tp_movimento', String(400)),
    Column('prmv_dt_ultima_atualizacao', DateTime()),
    Column('prmv_hash', String(32)),
    Column('prmv_tx_inteiro_teor', LargeBinary())
)


TB_ITEM_MOVIMENTO = Table(
    'tjrj_movimento_item_tj',
    meta,
    Column('mvit_dk', Integer, primary_key=True),
    Column('mvit_prmv_dk', Integer()),
    Column('mvit_tp_chave', String(256)),
    Column('mvit_tp_valor', String(4000)),
)
