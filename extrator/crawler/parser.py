from slugify import slugify

from .utils import limpa_conteudo


def parse_metadados(linhas_de_dados, numero_processo, inicio_metadados,
                    fim_metadados):
    metadados = {
        'status': [''],
        'comarca': [''],
        'endereco': [''],
        'bairro': [''],
        'cidade': [''],
        'acao': [''],
        'assunto': [''],
        'classe': [''],
        'livro': [''],
        'folha': [''],
        'numero-do-tombo': [''],
        'aviso-ao-advogado': [''],
        'autor': [''],
        'requerido': [''],
        'requerente': [''],
        'advogado-s': ['']
    }

    # Delimita o processo na regiao dos metadados
    linhas_com_metadados = linhas_de_dados[inicio_metadados:fim_metadados]

    metadados['numero-processo'] = numero_processo
    metadados['status'] = limpa_conteudo(
        linhas_com_metadados[0].find_all('td')[0].get_text()
    )

    # Apaga linhas utilizadas
    del linhas_com_metadados[:2]

    comarcas = []
    comecou_comarca = False
    for tr in list(linhas_com_metadados):
        linhas_com_metadados.pop(0)
        colunas = tr.find_all('td')
        dados = ''.join([c.get_text() for c in colunas])
        if 'Comarca' in dados or \
           'Regional' in dados:
            comecou_comarca = True

        if comecou_comarca:
            comarcas += extrai_dados_colunas(colunas)

        if len(colunas) == 1 and comecou_comarca:
            break

    metadados['comarca'] = comarcas

    for tr in list(linhas_com_metadados):
        linhas_com_metadados.pop(0)
        linha = []
        colunas = tr.find_all('td')
        linha = extrai_dados_colunas(colunas)
        if linha:
            metadados[slugify(linha[0])] = linha[1:]

    return metadados


def area_dos_metadados(linhas_de_dados):
    # Aparentemente esse valor e fixo
    inicio = 0
    for indice, linha in enumerate(linhas_de_dados):
        coluna = linha.find('td')
        atributos_inicio_metadados = {'align': 'center',
                                      'class': ['negrito'],
                                      'colspan': '2'}
        if not inicio and coluna.attrs == atributos_inicio_metadados:
            inicio = indice

        if 'Tipo do Movimento:' in linha.get_text():
            fim = indice - 1
            break

    return inicio, fim


def extrai_dados_colunas(colunas):
    linha = []
    for td in colunas:
        linha += list(
            filter(None, [limpa_conteudo(td.get_text()) if td else ''])
        )

    return linha
