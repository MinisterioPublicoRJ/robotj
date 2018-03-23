import re

from hashlib import md5


def formata_numero_processo(numero_processo):
    mascara = "{0}-{1}.{2}.{3}.{4}.{5}"

    primeira_parte = slice(0, 7)
    segunda_parte = slice(7, 9)
    terceira_parte = slice(9, 13)
    quarta_parte = slice(13, 14)
    quinta_parte = slice(14, 16)
    sexta_parte = slice(16, 20)

    return mascara.format(
        numero_processo[primeira_parte],
        numero_processo[segunda_parte],
        numero_processo[terceira_parte],
        numero_processo[quarta_parte],
        numero_processo[quinta_parte],
        numero_processo[sexta_parte]
    )


def limpa_conteudo(conteudo_sujo):
    return re.sub('\s+', ' ', conteudo_sujo).strip()


def confere_atualizao(hash_inicial, processo):
    return True if hash_inicial != md5(processo).hexdigest() else False


def remove_data_consulta(html):
    html = html.decode('latin-1')
    return re.sub(
        'TJ/RJ -\r\n                      \d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}',
        '',
        html).encode()
