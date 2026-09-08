from flask import jsonify


def index():
    return jsonify({
        'mensagem': 'API de imóveis funcionando'
    }), 200