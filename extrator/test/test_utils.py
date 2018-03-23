from unittest import TestCase

from ..crawler.utils import (formata_numero_processo,
                             limpa_conteudo,
                             confere_atualizao,
                             remove_data_consulta,
                             cria_hash_do_movimento)
from .fixtures.processos import processo_judicial_1


class Utils(TestCase):
    def test_format_document_numner(self):
        numero_processo = "09878976543451238976"

        numero_processo_formatado = formata_numero_processo(numero_processo)
        expected = "0987897-65.4345.1.23.8976"

        self.assertEqual(numero_processo_formatado, expected)

    def test_limpa_conteudo(self):
        conteudo_sujo = ('\r\n                        Av. Presidente Lincol'
                         'n\r\n                        \xa0\r\n            '
                         '            857\r\n                        \xa0\r'
                         '\n                        \r\n                   '
                         '\xa0\r\n                      ')

        conteudo_limpo = limpa_conteudo(conteudo_sujo)
        esperado = 'Av. Presidente Lincoln 857'

        self.assertEqual(conteudo_limpo, esperado)


class Hash(TestCase):
    def test_hash_diferente_para_atualizacao_no_processo(self):
        """
            Cada processo tera uma identificcao hash inicial.
            Caso a hash inicial seja diferente da hash calculada
            novamente no mesmo documento, houve alteracao no processo.
        """
        hash_inicial = '8a1586a2c0795b9e4abfb7f9af914cc4'
        processo_alterado = processo_judicial_1 + b'a'
        foi_atualizado = confere_atualizao(hash_inicial, processo_alterado)

        self.assertTrue(foi_atualizado)

    def test_hash_igual_para_processo_inalterado(self):
        hash_inicial = '8a1586a2c0795b9e4abfb7f9af914cc4'
        foi_atualizado = confere_atualizao(hash_inicial, processo_judicial_1)

        self.assertFalse(foi_atualizado)

    def test_remove_data_de_consulta_do_html(self):
        trecho_processo = '<tr valign="top"><td colspan="2" class="info">'\
            'TJ/RJ -\r\n                      23/03/2018 12:48:23</td>'\
            '</tr>'.encode()

        processo_sem_data = remove_data_consulta(trecho_processo)
        esperado = '<tr valign="top"><td colspan="2" class="info"></td>'\
            '</tr>'.encode()

        self.assertEqual(processo_sem_data, esperado)

    def test_cria_hash_para_um_movimento(self):
        item = {
            'tipo-do-movimento': 'Conclusão ao Juiz',
            'data-da-conclusao': ['21/10/2015'],
            'juiz': ['VIVIANE TOVAR DE MATTOS ABRAHAO']
        }

        movimento_hash = cria_hash_do_movimento(item)
        esperado = '03b979f3d68a8b526746c94370039ddb'

        self.assertEqual(movimento_hash, esperado)
