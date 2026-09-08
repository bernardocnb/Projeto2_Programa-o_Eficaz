from flask import Flask

import views


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return views.index()


@app.route('/imoveis', methods=['GET'])
def listar_imoveis():
    return views.listar_imoveis()


if __name__ == '__main__':
    app.run(debug=True)