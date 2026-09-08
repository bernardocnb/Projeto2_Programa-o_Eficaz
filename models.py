from database.connection import get_connection


CAMPOS_IMOVEL = [
    'id',
    'logradouro',
    'tipo_logradouro',
    'bairro',
    'cidade',
    'cep',
    'tipo',
    'valor',
    'data_aquisicao'
]


def converter_linha_em_imovel(linha):
    if isinstance(linha, dict):
        imovel = dict(linha)
    else:
        imovel = dict(zip(CAMPOS_IMOVEL, linha))

    if imovel['valor'] is not None:
        imovel['valor'] = float(imovel['valor'])

    data = imovel['data_aquisicao']

    if hasattr(data, 'isoformat'):
        imovel['data_aquisicao'] = data.isoformat()

    return imovel


def listar_imoveis():
    conexao = get_connection()
    cursor = conexao.cursor()

    consulta = '''
        SELECT
            id,
            logradouro,
            tipo_logradouro,
            bairro,
            cidade,
            cep,
            tipo,
            valor,
            data_aquisicao
        FROM imoveis
    '''

    try:
        cursor.execute(consulta)
        linhas = cursor.fetchall()

        imoveis = []

        for linha in linhas:
            imovel = converter_linha_em_imovel(linha)
            imoveis.append(imovel)

        return imoveis
    finally:
        cursor.close()
        conexao.close()