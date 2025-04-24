from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///compras.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo da tabela de compras
class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(20), nullable=False)
    whatsapp = db.Column(db.String(20), nullable=False)
    mail = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    cep = db.Column(db.String(20), nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)
    itens = db.Column(db.Text, nullable=False)  # Armazena o carrinho como JSON em texto

# Rota de teste
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"mensagem": "API funcionando corretamente!"})

# Rota para registrar compra
@app.route("/compras", methods=["POST"])
def registrar_compra():
    dados = request.get_json()

    nova_compra = Compra(
        nome=dados["nome"],
        cpf=dados["cpf"],
        whatsapp=dados["whatsapp"],
        mail=dados["mail"],
        endereco=dados["endereco"],
        cep=dados["cep"],
        valor_total=dados["valor_total"],
        forma_pagamento=dados["forma_pagamento"],
        itens=dados["itens"]  # Recebe string JSON com os produtos
    )

    db.session.add(nova_compra)
    db.session.commit()

    return jsonify({"mensagem": "Compra registrada com sucesso!"})

# Inicializar o banco de dados
from app import app, db

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Banco de dados resetado com sucesso!")
    
if __name__ == "__main__":
    app.run(debug=True)
