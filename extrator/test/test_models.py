from unittest import TestCase
from unittest.mock import patch, MagicMock
from ..datasources.models import (
    _itens_não_presentes,
    obtem_hashs_movimentos,
    insere_movimento
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

    def test_itens_nao_presentes(self):
        itens_no_banco = ['123', '456']

        assert len(_itens_não_presentes(self.itens, itens_no_banco)) == 2

    def test_todos_itens_presentes(self):
        itens_no_banco = ['123', '456', '789', '012']

        assert not _itens_não_presentes(self.itens, itens_no_banco)

    def test_item_extra_presente(self):
        itens_no_banco = ['123', '456', '789', '012', '444']

        assert not _itens_não_presentes(self.itens, itens_no_banco)

    @patch('robotj.extrator.datasources.models.TB_MOVIMENTO_PROCESSO')
    def test_obtem_hashs_movimentos(self, tb_movimento):
        select_mock = MagicMock()
        select_mock.where.return_value = [('123',), ('456',)]
        tb_movimento.select.return_value = select_mock

        hashs = obtem_hashs_movimentos('3')

        assert hashs == ['123', '456']

    @patch('robotj.extrator.datasources.models._insere_movimento')
    @patch('robotj.extrator.datasources.models._insere_item_movimento')
    def test_inserir_movimento(self, _insere_item_movimento, _insere_movimento):
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
