from flask import jsonify

import models


def index():
    return jsonify({
        'mensagem': 'API de imoveis funcionando'
    }), 200


def listar_imoveis(tipo=None, cidade=None):
    if tipo:
        imoveis = models.buscar_imoveis_por_tipo(tipo)
    elif cidade:
        imoveis = models.buscar_imoveis_por_cidade(cidade)
    else:
        imoveis = models.listar_imoveis()

    return jsonify(imoveis), 200

def buscar_imovel_por_id(imovel_id):
    imovel = models.buscar_imovel_por_id(imovel_id)

    if imovel is None:
        return jsonify({
            'erro': 'Imóvel não encontrado'
        }), 404

    return jsonify(imovel), 200
    