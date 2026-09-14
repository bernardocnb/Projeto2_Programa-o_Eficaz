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


def buscar_imovel_por_id(imovel_id):
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
        WHERE id = %s
    '''

    try:
        cursor.execute(consulta, (imovel_id,))
        linha = cursor.fetchone()

        if linha is None:
            return None

        return converter_linha_em_imovel(linha)
    finally:
        cursor.close()
        conexao.close()


def buscar_imoveis_por_tipo(tipo):
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
        WHERE tipo = %s
    '''

    try:
        cursor.execute(consulta, (tipo,))
        linhas = cursor.fetchall()

        return [
            converter_linha_em_imovel(linha)
            for linha in linhas
        ]
    finally:
        cursor.close()
        conexao.close()


def buscar_imoveis_por_cidade(cidade):
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
        WHERE cidade = %s
    '''

    try:
        cursor.execute(consulta, (cidade,))
        linhas = cursor.fetchall()

        return [
            converter_linha_em_imovel(linha)
            for linha in linhas
        ]
    finally:
        cursor.close()
        conexao.close()

def adicionar_imovel(dados):
    conexao = get_connection()
    cursor = conexao.cursor()

    comando = '''
        INSERT INTO imoveis (
            logradouro,
            tipo_logradouro,
            bairro,
            cidade,
            cep,
            tipo,
            valor,
            data_aquisicao
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''

    valores = (
        dados['logradouro'],
        dados['tipo_logradouro'],
        dados['bairro'],
        dados['cidade'],
        dados['cep'],
        dados['tipo'],
        dados['valor'],
        dados['data_aquisicao']
    )

    try:
        cursor.execute(comando, valores)
        conexao.commit()

        return {
            'id': cursor.lastrowid,
            **dados
        }
    except Exception:
        conexao.rollback()
        raise
    finally:
        cursor.close()
        conexao.close()