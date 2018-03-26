from unittest import TestCase
from ..datasources.mcpr import _itens_não_presentes


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
