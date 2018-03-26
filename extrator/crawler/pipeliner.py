import requests
from bs4 import BeautifulSoup
from .utils import formata_numero_processo, cria_hash_do_processo
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
    try:
        inicio, fim = area_dos_metadados(linhas)
        dados_processo.update(
            parse_metadados(
                linhas,
                numero_processo,
                inicio,
                fim))
        dados_processo['hash'] = cria_hash_do_processo(resp.content)
        dados_processo.update(parse_itens(soup, numero_processo, inicio + 1))
    except Exception as erro:
        logger().error(
            "Erro de parsing do processo - {0}, com mensagem: {1}".format(
                numero_processo,
                erro))
    return dados_processo
