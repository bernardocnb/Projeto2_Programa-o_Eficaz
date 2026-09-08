def validar_campos(dados, campos_obrigatorios):
    for campo in campos_obrigatorios:
        if campo not in dados:
            return False

    return True