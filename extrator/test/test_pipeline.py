from unittest.mock import patch, call, MagicMock
from unittest import TestCase
from ..crawler.pipeliner import pipeline


class Pipeline(TestCase):
    @patch('robotj.extrator.crawler.pipeliner.parse_itens',
           side_effect=[{'d': 4}, {'e': 5}, {'f': 6}])
    @patch('robotj.extrator.crawler.pipeliner.parse_metadados',
           side_effect=[{'a': 1}, {'b': 2}, {'c': 3}])
    @patch('robotj.extrator.crawler.pipeliner.area_dos_metadados',
           side_effect=[(0, 1), (2, 3), (4, 5)])
    @patch('robotj.extrator.crawler.pipeliner.BeautifulSoup')
    @patch('robotj.extrator.crawler.pipeliner.requests')
    @patch('robotj.extrator.crawler.pipeliner.formata_numero_processo')
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

        processos = [processo for processo in pipeline(lista_de_processos)]

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
