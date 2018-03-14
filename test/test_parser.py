from unittest import TestCase

from bs4 import BeautifulSoup

from robotj.crawler.parser import (parse_metadados,
                                   area_dos_metadados,
                                   extrai_dados_colunas)
from robotj.test.processos import processo_judicial_1, processo_judicial_2


class Parser(TestCase):
    def _prepara_html(self, html):
        soup_obj = BeautifulSoup(html)
        return soup_obj.find_all('tr')

    def _test_parse_metadados_processo_judicial(self):
        metadados = parse_metadados(
            self._prepara_html(processo_judicial_1),
            '0004999-58.2015.8.19.0036',
            inicio_metadados=6,
            fim_metadados=26
        )

        expected = {
            'numero_processo': '0004999-58.2015.8.19.0036',
            'status': 'PROCESSO COM BAIXA',
            'comarca': [
                'Comarca de Nilópolis',
                '2ª Vara de Família e da Infância e da Juventude e do Idoso',
                'Cartório da 2ª Vara de Família, Inf. e da Juv. e do Idoso'],
            'endereco': ['Getúlio Vargas 571 - 6º andar'],
            'bairro': ['Olinda'],
            'aviso-ao-advogado': [''],
            'cidade': ['Nilópolis'],
            'acao': [('Medidas Pertinentes Aos Pais Ou '
                     'Responsável / Seção Cível')],
            'assunto': [('Medidas Pertinentes Aos Pais Ou Responsável'
                         ' / Seção Cível')],
            'classe': [('Perda ou Suspensão ou Restabelecimento do Poder '
                        'Familiar')],
            'autor': ['MINISTÉRIO PÚBLICO DO ESTADO DO RIO DE JANEIRO'],
            'requerido': ['DANIELLE MARIA GOMES BARBOSA'],
            'requerente': [''],
            'advogado-s': ['TJ000002 - DEFENSOR PÚBLICO']}

        for chave, valor in expected.items():
            with self.subTest():
                self.assertEqual(metadados[chave], valor)

    def test_parse_metadados_de_outro_processo_com_outras_informacoes(self):
        metadados = parse_metadados(
            self._prepara_html(processo_judicial_2),
            '0025375-16.2012.8.19.0054',
            inicio_metadados=6,
            fim_metadados=27
        )

        expected = {
            'numero_processo': '0025375-16.2012.8.19.0054',
            'status': 'ARQUIVADO EM DEFINITIVO - MAÇO Nº 722, em 20/05/2013',
            'comarca': [
                'Comarca de São João de Meriti',
                'Juizado da Infância e Juventude e do Idoso',
                'Cartório do Juizado da Infância e Juventude e do Idoso'],
            'endereco': ['Av. Presidente Lincoln 857'],
            'bairro': ['Vilar dos Teles'],
            'cidade': ['São João de Meriti'],
            'acao': ['Entrada e Permanência de Menores / Seção Cível'],
            'assunto': ['Entrada e Permanência de Menores / Seção Cível'],
            'classe': ['Autorização judicial - ECA'],
            'aviso-ao-advogado': ['tem peça na pasta.'],
            'autor': [''],
            'requerido': [''],
            'requerente': ['IGREJA EVANGÉLICA NOVA ASSEMBLÉIA DE DEUS'],
            'advogado-s': ['RJ081634 - IRANY SPERANDIO DE MEDEIROS']}

        for chave, valor in expected.items():
            with self.subTest():
                self.assertEqual(metadados[chave], valor)

    def test_delimita_linhas_dos_metadados_processo_judicial_1(self):
        inicio, fim = area_dos_metadados(
            self._prepara_html(processo_judicial_1)
        )

        inicio_esperado = 6
        fim_esperado = 26

        self.assertEqual(inicio, inicio_esperado)
        self.assertEqual(fim, fim_esperado)

    def test_extrai_dados_das_colunas(self):
        html = """
                <tr>
                 <td class="negrito" nowrap="" valign="top">Tipo:</td>
                 <td align="justify" class="normal" valign="top">Conclusão</td>
                 </tr>
                """
        soup = self._prepara_html(html)[0].find_all('td')
        dados_das_colunas = extrai_dados_colunas(soup)
        esperado = ['Tipo:', 'Conclusão']

        self.assertEqual(dados_das_colunas, esperado)
