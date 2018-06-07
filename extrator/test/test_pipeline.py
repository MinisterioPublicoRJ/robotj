from unittest.mock import patch, MagicMock
from unittest import TestCase
from ..crawler.pipeliner import pipeline
from ..settings import URL_PROCESSO


class Pipeline(TestCase):
    @patch('robotj.extrator.crawler.pipeliner.parse_itens',
           return_value={'d': 4})
    @patch('robotj.extrator.crawler.pipeliner.parse_metadados',
           return_value={'a': 1})
    @patch('robotj.extrator.crawler.pipeliner.area_dos_metadados',
           return_value=(0, 1))
    @patch('robotj.extrator.crawler.pipeliner.BeautifulSoup')
    @patch('robotj.extrator.crawler.pipeliner.cria_hash_do_processo')
    @patch('robotj.extrator.crawler.pipeliner.requests')
    @patch('robotj.extrator.crawler.pipeliner.formata_numero_processo')
    def test_pipeline_do_parsing_dos_processos(self, _fnp, _req, _chdp, _bs,
                                               _am, _pm, _pi):
        processo = '1234'
        numero_formatado = '1.2.3.4'
        html = '{"a": 1}'
        _resp_mock = MagicMock()
        _resp_mock.content = html

        _soup_mock = MagicMock()

        _soup_mock.find_all.return_value = 'rows_mock'

        _fnp.return_value = numero_formatado
        _req.get.return_value = _resp_mock
        _chdp.return_value = 'ab12'
        _bs.return_value = _soup_mock

        processos = pipeline(processo)

        _fnp.assert_called_once_with(processo)
        _req.get.assert_called_once_with(URL_PROCESSO.format(
            doc_number=numero_formatado),
            headers={'X-Forwarded-For': '10.0.250.15'})
        _chdp.assert_called_once_with(html)
        _bs.assert_called_once_with(html, 'lxml')
        _soup_mock.find_all.assert_called_once_with('tr')
        _am.assert_called_once_with('rows_mock')
        _pm.assert_called_once_with('rows_mock', '1.2.3.4', 0, 1)
        _pi.assert_called_once_with(_soup_mock, '1234', 1)

        self.assertEqual(processos, {'a': 1, 'd': 4, 'hash': 'ab12'})
