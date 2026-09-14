from flask import jsonify

import models
from utils import possui_campos_obrigatorios


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

def adicionar_imovel(dados):
    if dados is None:
        return jsonify({
            'erro': 'JSON inválido ou não enviado'
        }), 400

    if not possui_campos_obrigatorios(dados):
        return jsonify({
            'erro': 'Campos obrigatórios não foram informados'
        }), 400

    imovel_criado = models.adicionar_imovel(dados)

    return jsonify(imovel_criado), 201
