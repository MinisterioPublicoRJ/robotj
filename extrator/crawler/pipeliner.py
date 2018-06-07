import requests
import json
from bs4 import BeautifulSoup
from .utils import formata_numero_processo, cria_hash_do_processo
from .parser import parse_metadados, area_dos_metadados, parse_itens
from ..base.utils import logger
from ..settings import URL_PROCESSO


def pipeline(processo):
    logger().info(processo)
    dados_processo = {}
    numero_processo = formata_numero_processo(processo)
    try:
        resp = requests.get(URL_PROCESSO.format(
            doc_number=numero_processo),
            headers={'X-Forwarded-For': '10.0.250.15'})
        soup = BeautifulSoup(resp.content, 'lxml')
        linhas = soup.find_all('tr')
        inicio, fim = area_dos_metadados(linhas)
        dados_processo.update(
            parse_metadados(
                linhas,
                numero_processo,
                inicio,
                fim))
        dados_processo['hash'] = cria_hash_do_processo(
            json.dumps(dados_processo))
        dados_processo.update(parse_itens(soup, processo, inicio + 1))
    except Exception as erro:
        logger().error(
            "Erro de parsing do processo - {0}, com mensagem: {1}".format(
                numero_processo,
                erro))
        raise erro
    return dados_processo
