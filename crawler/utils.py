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
