from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, LargeBinary

meta = MetaData()

TB_DOCUMENTO = Table(
    'nome_tabela',
    meta,
    Column('id', Integer, primary_key=True),
    Column('executado', String(256)),
    Column('advogado_s', String(256)),
    Column('numero_do_tombo', String(256)),
    Column('oficio_de_registro', String(256)),
    Column('folha', String(256)),
    Column('requerido', String(256)),
    Column('exequente', String(256)),
    Column('representante_legal', String(256)),
    Column('acao', String(256)),
    Column('comunicante', String(256)),
    Column('requerente', String(256)),
    Column('bairro', String(256)),
    Column('livro', String(256)),
    Column('pai', String(256)),
    Column('mae', String(256)),
    Column('aviso_ao_advogado', String(256)),
    Column('status', String(256)),
    Column('comarca', String(256)),
    Column('assistente', String(256)),
    Column('cidade', String(256)),
    Column('autor_do_fato', String(256)),
    Column('acusado', String(256)),
    Column('impetrado', String(256)),
    Column('impetrante', String(256)),
    Column('notificado', String(256)),
    Column('autor', String(256)),
    Column('intimado', String(256)),
    Column('idoso', String(256)),
    Column('avo_avo', String(256)),
    Column('numero_processo', String(256)),
    Column('reu', String(256)),
    Column('reclamado', String(256)),
    Column('endereco', String(256)),
    Column('prazo', String(256)),
    Column('classe', String(256)),
    Column('assunto', String(256)),
    Column('data_ultima_atualizacao', DateTime()),
    Column('data_ultima_vista', DateTime()),
    Column('hash', String(32)),
)


TB_MOVIMENTO = Table(
    'nome_movimento',
    meta,
    Column('id', Integer, primary_key=True),
    Column('id_documento', Integer),
    Column('tipo_do_movimento', String(256)),
    Column('data_ultima_atualizacao', DateTime()),
    Column('hash', String(32)),
)


TB_ITEM_MOVIMENTO = Table(
    'nome_item_movimento',
    meta,
    Column('id', Integer, primary_key=True),
    Column('id_movimento', Integer),
    Column('chave', String(256)),
    Column('valor', DateTime()),
    Column('inteiro_teor', LargeBinary()),
    Column('hash', String(32)),
)
