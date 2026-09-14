def validar_campos(dados, campos_obrigatorios):
    for campo in campos_obrigatorios:
        if campo not in dados:
            return False

    return True


CAMPOS_OBRIGATORIOS = [
    'logradouro',
    'tipo_logradouro',
    'bairro',
    'cidade',
    'cep',
    'tipo',
    'valor',
    'data_aquisicao'
]


def possui_campos_obrigatorios(dados):
    return all(campo in dados for campo in CAMPOS_OBRIGATORIOS)