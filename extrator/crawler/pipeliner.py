import requests
from bs4 import BeautifulSoup
from .utils import formata_numero_processo
from .parser import parse_metadados, area_dos_metadados, parse_itens
from ..base.utils import logger


URL = "http://www4.tjrj.jus.br/consultaProcessoWebV2/consultaMov.do?v=2"\
      "&numProcesso={doc_number}&acessoIP=internet&tipoUsuario"


def pipeline(processo):
    logger().info(processo)
    dados_processo = {}
    numero_processo = formata_numero_processo(processo)
    resp = requests.get(URL.format(doc_number=numero_processo))
    soup = BeautifulSoup(resp.content, 'lxml')
    linhas = soup.find_all('tr')
    inicio, fim = area_dos_metadados(linhas)
    dados_processo.update(parse_metadados(linhas, numero_processo, inicio,
                                          fim))
    dados_processo.update(parse_itens(soup, numero_processo, inicio + 1))
    return dados_processo
