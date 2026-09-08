from flask import jsonify

import models


def index():
    return jsonify({
        'mensagem': 'API de imóveis funcionando'
    }), 200


def listar_imoveis():
    imoveis = models.listar_imoveis()

    return jsonify(imoveis), 200