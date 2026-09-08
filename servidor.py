from flask import Flask
import views


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return views.index()


if __name__ == '__main__':
    app.run(debug=True)