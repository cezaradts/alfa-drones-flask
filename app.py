from flask import Flask, jsonify, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para contatos
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    mensagem = db.Column(db.Text)

# Modelo para compras
class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)

with app.app_context():
 
    db.create_all()

@app.route("/")
def index():
    return jsonify({"mensagem": "API Alfa Drones está funcionando!"})

@app.route("/test")
def test():
    return jsonify({"status": "OK", "mensagem": "Rota de teste funcionando perfeitamente!"})

@app.route("/contato", methods=["POST"])
def contato():
    dados = request.get_json()
    nome = dados.get("nome")
    email = dados.get("email")
    telefone = dados.get("telefone")
    mensagem = dados.get("mensagem")

    novo = Contato(nome=nome, email=email, telefone=telefone, mensagem=mensagem)
    db.session.add(novo)
    db.session.commit()

    return jsonify({"mensagem": "Contato enviado com sucesso!"})

@app.route("/contatos", methods=["GET"])
def listar_contatos():
    contatos = Contato.query.all()
    resultado = []
    for c in contatos:
        resultado.append({
            "id": c.id,
            "nome": c.nome,
            "email": c.email,
            "telefone": c.telefone,
            "mensagem": c.mensagem
        })
    return jsonify(resultado)

# Rota POST de compra com dados enviados por JSON
@app.route("/compras", methods=["POST"])
def registrar_compra():
    dados = request.get_json()
    nova = Compra(
        nome_completo=dados.get("nome"),
        endereco=dados.get("endereco"),
        cpf=dados.get("cpf"),
        cep=dados.get("cep"),
        valor_total=dados.get("valor_total"),
        forma_pagamento=dados.get("forma_pagamento")
    )
    db.session.add(nova)
    db.session.commit()
    return jsonify({"mensagem": "Compra registrada com sucesso!", "id": nova.id}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

# Rota GET para listar todas as compras
@app.route("/compras", methods=["GET"])
def listar_compras():
    compras = Compra.query.all()
    resultado = []
    for c in compras:
        resultado.append({
            "id": c.id,
            "nome_completo": c.nome_completo,
            "endereco": c.endereco,
            "cpf": c.cpf,
            "cep": c.cep,
            "valor_total": c.valor_total,
            "forma_pagamento": c.forma_pagamento
        })
    return jsonify(resultado)

# Rota para exibir relatório de uma compra
@app.route("/relatorio/<int:id>")
def relatorio(id):
    compra = Compra.query.get_or_404(id)
    return render_template("relatorio.html", compra=compra)
