from unittest import TestCase
from unittest.mock import patch, call, MagicMock

from bs4 import BeautifulSoup

from ..crawler.parser import (parse_metadados,
                              area_dos_metadados,
                              extrai_dados_colunas,
                              parse_itens,
                              pipeline)
from .fixtures.processos import (processo_judicial_1,
                                 processo_judicial_2,
                                 processo_judicial_3,
                                 processo_judicial_4,
                                 processo_judicial_5,
                                 processo_judicial_6,
                                 processo_judicial_7)


def _prepara_html(html):
    soup_obj = BeautifulSoup(html, 'lxml')
    return soup_obj.find_all('tr')


class ParserMetadados(TestCase):

    def _test_parse_metadados_processo_judicial(self):
        metadados = parse_metadados(
            _prepara_html(processo_judicial_1),
            '0004999-58.2015.8.19.0036',
            inicio_metadados=6,
            fim_metadados=26
        )

        expected = {
            'numero-processo': '0004999-58.2015.8.19.0036',
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
            _prepara_html(processo_judicial_2),
            '0025375-16.2012.8.19.0054',
            inicio_metadados=6,
            fim_metadados=27
        )

        expected = {
            'numero-processo': '0025375-16.2012.8.19.0054',
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
            'livro': [''],
            'folha': [''],
            'numero-do-tombo': [''],
            'requerido': [''],
            'requerente': ['IGREJA EVANGÉLICA NOVA ASSEMBLÉIA DE DEUS'],
            'advogado-s': ['RJ081634 - IRANY SPERANDIO DE MEDEIROS']}

        for chave, valor in expected.items():
            with self.subTest():
                self.assertEqual(metadados[chave], valor)

    def test_parsea_processo_com_informacoes_de_comarca_diferentes(self):
        metadados = parse_metadados(
            _prepara_html(processo_judicial_3),
            '0001762-56.2009.8.19.0026',
            inicio_metadados=7,
            fim_metadados=23
        )

        esperado = {
            'numero-processo': '0001762-56.2009.8.19.0026',
            'status': 'ARQUIVADO EM DEFINITIVO - MAÇO Nº 1903, em 22/11/2012',
            'comarca': [
                'Comarca de Itaperuna',
                'Vara de Família e da Infância e da Juventude e do Idoso',
                'Cartório da Vara de Família, Inf. e da Juv. e do Idoso'],
            'endereco': ['Rodovia Br-356 Km 01'],
            'bairro': [''],
            'cidade': ['Itaperuna'],
            'acao': ['Adoção de Criança / Seção Cível'],
            'assunto': ['Adoção de Criança / Seção Cível'],
            'classe': ['Adoção c/c Destituição do Poder Familiar - ECA'],
            'aviso-ao-advogado': [''],
            'autor': [''],
            'requerido': [''],
            'requerente': [''],
            'advogado-s': ['RJ146889 - VIRGINIA MARIA RAMOS DA FONSECA']}

        for chave, valor in esperado.items():
            with self.subTest():
                self.assertEqual(metadados[chave], valor)

    def test_parsea_processo_com_link_nos_metadados(self):
        metadados = parse_metadados(
            _prepara_html(processo_judicial_4),
            '0441870-74.2008.8.19.0001',
            inicio_metadados=7,
            fim_metadados=27
        )

        esperado = {
            'numero-processo': '0441870-74.2008.8.19.0001',
            'status': 'ARQUIVADO EM DEFINITIVO - MAÇO Nº 9819, em 24/02/2013',
            'comarca': [
                'Comarca da Capital',
                '1ª Vara da Infância da Juventude e do Idoso',
                'Cartório da 1ª Vara da Infância, da Juventude e do Idoso'],
            'endereco': ['Praça Onze de Junho 403 Praça Onze'],
            'bairro': ['Centro'],
            'cidade': ['Rio de Janeiro'],
            'acao': [''],
            'assunto': ['Adoção Nacional / Seção Cível'],
            'classe': ['Adoção c/c Destituição do Poder Familiar - ECA'],
            'aviso-ao-advogado': [''],
            'autor': [''],
            'requerido': ['MARIA GISLEUDA RODRIGUES DA SILVA'],
            'requerente': ['FRANCISCO CAMILO RIBEIRO e outro(s)...'],
            'advogado-s': ['TJ000002 - DEFENSOR PÚBLICO']}

        for chave, valor in esperado.items():
            with self.subTest():
                self.assertEqual(metadados[chave], valor)

    def test_parsea_processo_com_link_antes_dos_metadados(self):
        metadados = parse_metadados(
            _prepara_html(processo_judicial_5),
            '0001394-96.2011.8.19.0084',
            inicio_metadados=0,
            fim_metadados=23
        )

        esperado = {
            'numero-processo': '0001394-96.2011.8.19.0084',
            'status': '',
            'comarca': [
                'Comarca de Carapebus / Quissamã',
                'Vara Única',
                'Cartório da Vara Única'],
            'endereco': ['Estrada do Correio Imperial 1003'],
            'bairro': ['Piteiras'],
            'cidade': ['Quissamã'],
            'acao': ['Medidas Pertinentes Aos Pais Ou Responsável /'
                     ' Seção Cível'],
            'assunto': ['Medidas Pertinentes Aos Pais Ou Responsável /'
                        ' Seção Cível'],
            'classe': ['Apuração de Infração Administrativa às Normas de'
                       ' Proteção'],
            'aviso-ao-advogado': [''],
            'autor': [''],
            'requerido': [''],
            'requerente': [''],
            'advogado-s': ['RJ125011 - ALBECIR RIBEIRO RJ143662 -'
                           ' PAULO ROMERO AQUINO BARBOSA']}

        for chave, valor in esperado.items():
            with self.subTest():
                self.assertEqual(metadados[chave], valor)

    def test_parsea_processo_com_nome_regional_ao_inves_de_comarca(self):
        metadados = parse_metadados(
            _prepara_html(processo_judicial_6),
            '0021491-54.2011.8.19.0202',
            inicio_metadados=6,
            fim_metadados=21
        )

        esperado = {
            'numero-processo': '0021491-54.2011.8.19.0202',
            'status': 'ARQUIVADO EM DEFINITIVO - MAÇO Nº 442, em 27/02/2012',
            'comarca': [
                'Regional de Madureira',
                '3ª Vara da Infância, da Juventude e do Idoso',
                'Cartório da 3ª Vara da Infância, da Juventude e do Idoso'],
            'endereco': ['Avenida Ernani Cardoso 152 2º andar'],
            'bairro': ['Cascadura'],
            'cidade': ['Rio de Janeiro'],
            'acao': ['Acolhimento Institucional de Crianças e'
                     ' Adolescentes/seção Cível'],
            'assunto': ['Acolhimento Institucional de Crianças e'
                        ' Adolescentes/seção Cível'],
            'classe': ['Providência - ECA'],
            'aviso-ao-advogado': [''],
            'autor': [''],
            'requerido': [''],
            'requerente': [''],
            'advogado-s': ['']}

        for chave, valor in esperado.items():
            with self.subTest():
                self.assertEqual(metadados[chave], valor)

    def test_delimita_linhas_dos_metadados_processo_judicial_1(self):
        inicio, fim = area_dos_metadados(
            _prepara_html(processo_judicial_1)
        )

        inicio_esperado = 6
        fim_esperado = 26

        self.assertEqual(inicio, inicio_esperado)
        self.assertEqual(fim, fim_esperado)

    def test_delimita_linhas_dos_metadados_processo_judicial_3(self):
        """
            O Processo judicial numero 3, diferente dos outros 2 presentes
            nas fixtures, inicia os metadados em uma linha diferente.
        """
        inicio, fim = area_dos_metadados(
            _prepara_html(processo_judicial_3)
        )

        inicio_esperado = 7
        fim_esperado = 23

        self.assertEqual(inicio, inicio_esperado)
        self.assertEqual(fim, fim_esperado)

    def test_extrai_dados_das_colunas(self):
        html = """
                <tr>
                 <td class="negrito" nowrap="" valign="top">Tipo:</td>
                 <td align="justify" class="normal" valign="top">Conclusão</td>
                 </tr>
                """
        soup = _prepara_html(html)[0].find_all('td')
        dados_das_colunas = extrai_dados_colunas(soup)
        esperado = ['Tipo:', 'Conclusão']

        self.assertEqual(dados_das_colunas, esperado)


class ComparaItensProcessoMixin:
    def assert_items_equal(self, first, second):
        self.assertEqual(first['numero-processo'], second['numero-processo'])
        items_first = first['itens']
        items_second = second['itens']

        self.assertEqual(len(items_first), len(items_second))

        for item_first, item_second in zip(items_first, items_second):
            for key, value in item_second.items():
                with self.subTest():
                    self.assertEqual(item_first[key], value)


class ParserItems(ComparaItensProcessoMixin, TestCase):
    def test_extrai_itens_do_processo_judicial_1(self):
        soup = BeautifulSoup(processo_judicial_1, 'lxml')
        itens = parse_itens(
            soup,
            '0004999-58.2015.8.19.0036',
            inicio_itens=26
        )
        esperado = {
            'numero-processo':
            '0004999-58.2015.8.19.0036',
            'itens': [{
                'tipo-do-movimento':
                'Declínio de Competência',
                'data':
                '11/01/2016',
                'descricao':
                'VIJI DA COMARCA DE SÃO MATHEUS - ESPIRITO SANTOS'
            }, {
                'tipo-do-movimento': 'Recebimento',
                'data-de-recebimento': '19/11/2015'
            }, {
                'tipo-do-movimento':
                'Decisão - Declínio de Competência',
                'data-decisao':
                '21/10/2015',
                'descricao': ('Ante o teor de fls. 104, DECLINO DE MINHA'
                              ' COMPETÊNCIA para o Juízo da Infância e'
                              ' Juventude da Comarca de São Mateus, no'
                              ' Espírito Santo. Dê-se baixa e encaminhem-se'
                              ' imediatamente, com as nossas homenagens.')
            }, {
                'tipo-do-movimento': 'Conclusão ao Juiz',
                'data-da-conclusao': '21/10/2015',
                'juiz': 'VIVIANE TOVAR DE MATTOS ABRAHAO'
            }, {
                'tipo-do-movimento': 'Decurso de Prazo',
                'data-do-movimento': '20/10/2015'
            }, {
                'tipo-do-movimento': 'Recebidos os autos',
                'data-do-recebimento': '20/10/2015'
            }, {
                'tipo-do-movimento': 'Remessa',
                'destinatario': 'Ministério Público',
                'data-da-remessa': '06/08/2015',
                'prazo': '15 dia(s)'
            }, {
                'tipo-do-movimento': 'Recebimento',
                'data-de-recebimento': '30/07/2015'
            }, {
                'tipo-do-movimento':
                'Despacho - Proferido despacho de mero expediente',
                'data-despacho':
                '28/07/2015',
                'descricao':
                'Dê-se vista ao Ministério Público.'
            }, {
                'tipo-do-movimento': 'Conclusão ao Juiz',
                'data-da-conclusao': '28/07/2015',
                'juiz': 'VIVIANE TOVAR DE MATTOS ABRAHAO'
            }, {
                'tipo-do-movimento': 'Decurso de Prazo',
                'data-do-movimento': '27/07/2015'
            }, {
                'tipo-do-movimento': 'Recebidos os autos',
                'data-do-recebimento': '21/07/2015'
            }, {
                'tipo-do-movimento': 'Remessa',
                'destinatario': 'Psicologia',
                'data-da-remessa': '17/07/2015',
                'prazo': '15 dia(s)'
            }, {
                'tipo-do-movimento': 'Recebidos os autos',
                'data-do-recebimento': '17/07/2015'
            }, {
                'tipo-do-movimento': 'Remessa',
                'destinatario': 'Assistente Social',
                'data-da-remessa': '15/06/2015',
                'prazo': '15 dia(s)'
            }, {
                'tipo-do-movimento': 'Recebimento',
                'data-de-recebimento': '22/05/2015'
            }, {
                'tipo-do-movimento':
                'Despacho - Proferido despacho de mero expediente',
                'data-despacho':
                '11/05/2015',
                'descricao': ('Atenda-se ao Ministério Público. Promovam-se os'
                              ' estudos social e psicológico com a demandada'
                              ' e os adolescentes.'),
                'inteiro-teor': ('Atenda-se ao Ministério Público. Promovam-se'
                                 '  os estudos social e psicológico com a'
                                 ' demandada e os adolescentes.'),
            }, {
                'tipo-do-movimento': 'Conclusão ao Juiz',
                'data-da-conclusao': '11/05/2015',
                'juiz': 'VIVIANE TOVAR DE MATTOS ABRAHAO'
            }, {
                'tipo-do-movimento': 'Recebidos os autos',
                'data-do-recebimento': '30/04/2015'
            }, {
                'tipo-do-movimento': 'Remessa',
                'destinatario': 'Ministério Público',
                'data-da-remessa': '08/04/2015',
                'prazo': '15 dia(s)'
            }, {
                'tipo-do-movimento': 'Recebimento',
                'data-de-recebimento': '27/03/2015'
            }, {
                'tipo-do-movimento':
                'Despacho - Proferido despacho de mero expediente',
                'data-despacho': '19/03/2015',
                'descricao': 'Dê-se vista ao Ministério Público.',
                'inteiro-teor': 'Dê-se vista ao Ministério Público.'
            }, {
                'tipo-do-movimento': 'Conclusão ao Juiz',
                'data-da-conclusao': '19/03/2015',
                'juiz': 'VIVIANE TOVAR DE MATTOS ABRAHAO'
            }, {
                'tipo-do-movimento': 'Distribuição Dirigida',
                'data-da-distribuicao': '19/03/2015',
                'serventia': ('Cartório da 2ª Vara de Família, Inf. e da'
                              ' Juv. e do Idoso - 2ª Vara de Família e da'
                              ' Infância e da Juventude e do Idoso'),
                'localizacao-na-serventia': 'Saída de Acervo'
            }]
        }

        self.assert_items_equal(itens, esperado)

    def test_extrai_itens_de_processo_com_links_sem_atributo_onclick(self):
        soup = BeautifulSoup(processo_judicial_7, 'lxml')
        itens = parse_itens(
            soup,
            '0002346-95.2011.8.19.0045',
            inicio_itens=26
        )
        esperado = {
            'numero-processo':
            '0004999-58.2015.8.19.0036',
            'itens': [{
                'tipo-do-movimento':
                'Distribuição Dirigida',
                'data-da-distribuicao':
                '14/03/2011',
                'serventia':
                'Cartório da 2ª Vara de Família, da Inf., da Juv. e do Idoso -'
                ' 2ª Vara de Família Infância e Juventude e do Idoso',
                'processo-s-apensado-s': '0000159-51.2010.8.19.0045',
                'processo-s-no-tribunal-de-justica':
                '0002346-95.2011.8.19.0045',
                'protocolo-s-no-tribunal-de-justica':
                '201500617620 - Data: 26/10/2015',
                'localizacao-na-serventia':
                'Aguardando Arquivamento'
            }]
        }

        for chave, valor in esperado['itens'][-1].items():
            with self.subTest():
                self.assertEqual(itens['itens'][-1][chave], valor)


class Pipeline(TestCase):
    @patch('robotj.extrator.crawler.parser.parse_itens',
           side_effect=[{'d': 4}, {'e': 5}, {'f': 6}])
    @patch('robotj.extrator.crawler.parser.parse_metadados',
           side_effect=[{'a': 1}, {'b': 2}, {'c': 3}])
    @patch('robotj.extrator.crawler.parser.area_dos_metadados',
           side_effect=[(0, 1), (2, 3), (4, 5)])
    @patch('robotj.extrator.crawler.parser.BeautifulSoup')
    @patch('robotj.extrator.crawler.parser.requests')
    @patch('robotj.extrator.crawler.parser.formata_numero_processo')
    def test_pipeline_do_parsing_dos_processos(self, _fnp, _req, _bs,
                                               _am, _pm, _pi):
        url_processo = "http://www4.tjrj.jus.br/consultaProcessoWebV2/"\
                       "consultaMov.do?v=2&numProcesso={doc_number}&"\
                       "acessoIP=internet&tipoUsuario"
        lista_de_processos = [
            '1234',
            '5678',
            '9012'
        ]

        numeros_formatados = ['1.2.3.4', '5.6.7.8', '9.0.1.2']
        htmls = ['html_1', 'html_2', 'html_3']
        _resp_mock_1 = MagicMock()
        _resp_mock_2 = MagicMock()
        _resp_mock_3 = MagicMock()
        _resp_mock_1.content = htmls[0]
        _resp_mock_2.content = htmls[1]
        _resp_mock_3.content = htmls[2]

        _soup_mock_1 = MagicMock()
        _soup_mock_2 = MagicMock()
        _soup_mock_3 = MagicMock()

        _soup_mock_1.find_all.return_value = 'rows_mock_1'
        _soup_mock_2.find_all.return_value = 'rows_mock_2'
        _soup_mock_3.find_all.return_value = 'rows_mock_3'

        _fnp.side_effect = numeros_formatados
        _req.get.side_effect = [_resp_mock_1, _resp_mock_2, _resp_mock_3]
        _bs.side_effect = [_soup_mock_1, _soup_mock_2, _soup_mock_3]

        processos = pipeline(lista_de_processos)

        _fnp_calls = [call('1234'), call('5678'), call('9012')]
        _req_calls = [
            call(url_processo.format(doc_number=doc)) for
            doc in numeros_formatados
        ]
        _bs_calls = [call(html, 'lxml') for html in htmls]
        _am_calls = [call('rows_mock_1'), call('rows_mock_2'),
                     call('rows_mock_3')]
        _pm_calls = [call('rows_mock_1', '1.2.3.4', 0, 1),
                     call('rows_mock_2', '5.6.7.8', 2, 3),
                     call('rows_mock_3', '9.0.1.2', 4, 5)]
        _pi_calls = [call(_soup_mock_1, '1.2.3.4', 1),
                     call(_soup_mock_2, '5.6.7.8', 3),
                     call(_soup_mock_3, '9.0.1.2', 5)]

        _fnp.assert_has_calls(_fnp_calls)
        _req.get.assert_has_calls(_req_calls)
        _bs.assert_has_calls(_bs_calls)
        _soup_mock_1.find_all.assert_called_once_with('tr')
        _soup_mock_2.find_all.assert_called_once_with('tr')
        _soup_mock_3.find_all.assert_called_once_with('tr')
        _am.assert_has_calls(_am_calls)
        _pm.assert_has_calls(_pm_calls)
        _pi.assert_has_calls(_pi_calls)

        self.assertEqual(len(processos), 3)
        self.assertEqual(processos[0], {'a': 1, 'd': 4})
        self.assertEqual(processos[1], {'b': 2, 'e': 5})
        self.assertEqual(processos[2], {'c': 3, 'f': 6})
