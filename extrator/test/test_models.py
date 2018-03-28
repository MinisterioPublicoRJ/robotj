from unittest import TestCase
from unittest.mock import patch, MagicMock
from ..datasources.models import (
    _itens_não_presentes,
    _obtem_hashs_movimentos,
    insere_movimento,
    atualizar_documento
)


class ItensMovimento(TestCase):
    def setUp(self):
        self.itens = [
            {'tipo-do-movimento': 'Declínio de Competência',
             'data': ['11/01/2016'],
             'descricao':
             ['VIJI DA COMARCA DE SÃO MATHEUS - ESPIRITO SANTOS'],
             'hash': '123'},
            {'tipo-do-movimento': 'Recebimento',
             'data-de-recebimento': ['19/11/2015'],
             'hash': '456'},
            {'tipo-do-movimento': 'Decisão - Declínio de Competência',
             'data-decisao': ['21/10/2015'],
             'descricao': ['Ante o teor de fls. 104, DECLINO DE MINHA'
                           ' COMPETÊNCIA para o Juízo da Infância e'
                           ' Juventude da Comarca de São Mateus, no'
                           ' Espírito Santo. Dê-se baixa e encaminhem-se'
                           ' imediatamente, com as nossas homenagens.'],
             'hash': '789'},
            {'tipo-do-movimento': 'Conclusão ao Juiz',
             'data-da-conclusao': ['21/10/2015'],
             'juiz': ['VIVIANE TOVAR DE MATTOS ABRAHAO'],
             'hash': '012'}
        ]

        self.documento = {
            'numero-processo':
            '00049995820158190036',
            'hash': '1234',
            'itens': [{
                'tipo-do-movimento': 'Distribuição Dirigida',
                'hash': '1234',
                'data-da-distribuicao': ['14/03/2011'],
                'serventia':
                ['Cartório da 2ª Vara de Família, da Inf., da Juv. '
                 'e do Idoso -'
                 ' 2ª Vara de Família Infância e Juventude e do Idoso'],
                'processo-s-apensado-s': ['0000159-51.2010.8.19.0045'],
                'processo-s-no-tribunal-de-justica':
                ['0002346-95.2011.8.19.0045'],
                'protocolo-s-no-tribunal-de-justica':
                ['201500617620 - Data: 26/10/2015'],
                'localizacao-na-serventia':
                ['Aguardando Arquivamento']
            }]
        }

    def test_itens_nao_presentes(self):
        itens_no_banco = ['123', '456']

        assert len(_itens_não_presentes(self.itens, itens_no_banco)) == 2

    def test_todos_itens_presentes(self):
        itens_no_banco = ['123', '456', '789', '012']

        assert not _itens_não_presentes(self.itens, itens_no_banco)

    def test_item_extra_presente(self):
        itens_no_banco = ['123', '456', '789', '012', '444']

        assert not _itens_não_presentes(self.itens, itens_no_banco)

    @patch('robotj.extrator.datasources.models.conn')
    @patch('robotj.extrator.datasources.models.TB_MOVIMENTO_PROCESSO')
    def test_obtem_hashs_movimentos(self, tb_movimento, conn):
        conn_mock = MagicMock()
        conn_mock.execute.return_value = [('123',), ('456',)]
        conn.return_value = conn_mock
        select_mock = MagicMock()
        select_mock.where.return_value = [('123',), ('456',)]
        tb_movimento.select.return_value = select_mock

        hashs = _obtem_hashs_movimentos('3')

        assert hashs == ['123', '456']

    @patch('robotj.extrator.datasources.models.conn')
    @patch('robotj.extrator.datasources.models._insere_movimento_db')
    @patch('robotj.extrator.datasources.models._insere_item_movimento_db')
    def test_inserir_movimento(
            self,
            _insere_item_movimento,
            _insere_movimento,
            conn):
        _insere_movimento.return_value = 1
        _insere_item_movimento.return_value = 1

        movimento = {
            'tipo-do-movimento': 'Movimento de Teste',
            'hash': '1234567890',
            'chave': 'valor'
        }

        resultado = insere_movimento(1, movimento)

        assert resultado == 1

        _insere_movimento.assert_called_once_with(1, movimento)
        _insere_item_movimento.assert_called_once_with(
            1,
            'chave',
            'valor')

    @patch('robotj.extrator.datasources.models.conn')
    @patch('robotj.extrator.datasources.models._itens_não_presentes')
    @patch('robotj.extrator.datasources.models.atualizar_vista')
    @patch('robotj.extrator.datasources.models._obter_por_numero_processo')
    @patch('robotj.extrator.datasources.models._atualizar_documento_db')
    @patch('robotj.extrator.datasources.models._insere_documento_db')
    @patch('robotj.extrator.datasources.models._obtem_hashs_movimentos')
    @patch('robotj.extrator.datasources.models.insere_movimento')
    def test_atualizar_documento_novo(
            self,
            insere_movimento,
            _obtem_hashs_movimentos,
            _insere_documento_db,
            _atualizar_documento_db,
            _obter_por_numero_processo,
            atualizar_vista,
            _itens_não_presentes,
            conn):

        docu_dk = 3

        _obter_por_numero_processo.return_value = None
        _insere_documento_db.return_value = 1
        _obtem_hashs_movimentos.return_value = []
        _itens_não_presentes.return_value = self.documento['itens']
        insere_movimento.return_value = None

        atualizar_documento(self.documento, docu_dk)

        assert not atualizar_vista.called
        assert not _atualizar_documento_db.called

        assert _insere_documento_db.called
        assert _obtem_hashs_movimentos.called
        assert _itens_não_presentes.called
        assert insere_movimento.called

    @patch('robotj.extrator.datasources.models.conn')
    @patch('robotj.extrator.datasources.models._itens_não_presentes')
    @patch('robotj.extrator.datasources.models.atualizar_vista')
    @patch('robotj.extrator.datasources.models._obter_por_numero_processo')
    @patch('robotj.extrator.datasources.models._atualizar_documento_db')
    @patch('robotj.extrator.datasources.models._insere_documento_db')
    @patch('robotj.extrator.datasources.models._obtem_hashs_movimentos')
    @patch('robotj.extrator.datasources.models.insere_movimento')
    def test_atualizar_documento_existente_igual(
            self,
            insere_movimento,
            _obtem_hashs_movimentos,
            _insere_documento_db,
            _atualizar_documento_db,
            _obter_por_numero_processo,
            atualizar_vista,
            _itens_não_presentes,
            conn):

        docu_dk = 3

        _obter_por_numero_processo.return_value = {'prtj_hash': '1234'}

        atualizar_documento(self.documento, docu_dk)

        assert atualizar_vista.called
        assert not _atualizar_documento_db.called
        assert not _insere_documento_db.called
        assert not _obtem_hashs_movimentos.called
        assert not _itens_não_presentes.called
        assert not insere_movimento.called

    @patch('robotj.extrator.datasources.models.conn')
    @patch('robotj.extrator.datasources.models._itens_não_presentes')
    @patch('robotj.extrator.datasources.models.atualizar_vista')
    @patch('robotj.extrator.datasources.models._obter_por_numero_processo')
    @patch('robotj.extrator.datasources.models._atualizar_documento_db')
    @patch('robotj.extrator.datasources.models._insere_documento_db')
    @patch('robotj.extrator.datasources.models._obtem_hashs_movimentos')
    @patch('robotj.extrator.datasources.models.insere_movimento')
    def test_atualizar_documento_existente_diferente(
            self,
            insere_movimento,
            _obtem_hashs_movimentos,
            _insere_documento_db,
            _atualizar_documento_db,
            _obter_por_numero_processo,
            atualizar_vista,
            _itens_não_presentes,
            conn):

        docu_dk = 3

        _obter_por_numero_processo.return_value = {
            'prtj_hash': '1134',
            'prtj_dk': 1}
        _obtem_hashs_movimentos.return_value = []
        _itens_não_presentes.return_value = self.documento['itens']
        insere_movimento.return_value = None

        atualizar_documento(self.documento, docu_dk)

        self.assertFalse(atualizar_vista.called)
        self.assertTrue(_atualizar_documento_db.called)

        self.assertFalse(_insere_documento_db.called)
        self.assertTrue(_obtem_hashs_movimentos.called)
        self.assertTrue(_itens_não_presentes.called)
        self.assertTrue(insere_movimento.called)
