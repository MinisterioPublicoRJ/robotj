from unittest import TestCase

from ..crawler.utils import formata_numero_processo, limpa_conteudo


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
