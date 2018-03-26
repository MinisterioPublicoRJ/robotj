from unittest import TestCase
from unittest.mock import patch, MagicMock
from ..datasources.mcpr import _itens_não_presentes, obtem_hashs_movimentos


class DataSourceMcpr(TestCase):
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

    @patch('robotj.extrator.datasources.mcpr.TB_MOVIMENTO')
    def test_obtem_hashs_movimentos(self, tb_movimento):
        select_mock = MagicMock()
        select_mock.where.return_value = [('123',), ('456',)]
        tb_movimento.select.return_value = select_mock

        hashs = obtem_hashs_movimentos('3')

        assert hashs == ['123', '456']
