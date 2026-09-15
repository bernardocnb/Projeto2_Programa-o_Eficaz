from flask import Flask, request

import views


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return views.index()


@app.route('/imoveis', methods=['GET'])
def listar_imoveis():
    tipo = request.args.get('tipo')
    cidade = request.args.get('cidade')
    return views.listar_imoveis(tipo, cidade)

@app.route('/imoveis', methods=['POST'])
def adicionar_imovel():
    dados = request.get_json(silent=True)

    return views.adicionar_imovel(dados)

@app.route('/imoveis/<int:imovel_id>', methods=['GET'])
def buscar_imovel_por_id(imovel_id):
    return views.buscar_imovel_por_id(imovel_id)

@app.route('/imoveis/<int:imovel_id>', methods=['PUT'])
def atualizar_imovel(imovel_id):
    dados = request.get_json(silent=True)

    return views.atualizar_imovel(imovel_id, dados)

@app.route('/imoveis/<int:imovel_id>', methods=['DELETE'])
def remover_imovel(imovel_id):
    return views.remover_imovel(imovel_id)

if __name__ == '__main__':
    app.run(debug=True)
