from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
import os
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo do banco de dados
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mensagem = db.Column(db.Text)

# Criação da tabela
with app.app_context():
    db.create_all()

# Rota raiz
@app.route("/")
def index():
    return jsonify({"mensagem": "API Alfa Drones está funcionando!"})

# Rota de teste
@app.route("/test")
def test():
    return jsonify({"status": "OK", "mensagem": "Rota de teste funcionando perfeitamente!"})

# Rota de envio de formulário de contato
@app.route("/contato", methods=["POST"])
def contato():
    dados = request.get_json()
    nome = dados.get("nome")
    email = dados.get("email")
    mensagem = dados.get("mensagem")

    novo = Contato(nome=nome, email=email, mensagem=mensagem)
    db.session.add(novo)
    db.session.commit()

    return jsonify({"mensagem": "Contato enviado com sucesso!"})

if __name__ == "__main__":
    app.run(debug=True)
