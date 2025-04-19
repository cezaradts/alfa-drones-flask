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
    produtos = db.Column(db.String(500), nullable=False)
    valor_total = db.Column(db.Float, nullable=False)

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
# compra sucesso
@app.route("/compra", methods=["POST"])
def compra():
    dados = request.get_json()
    nome = dados.get("nome_completo")
    email = dados.get("email_1")
    telefone = dados.get("telefone_1")
    mensagem = dados.get("valor_compra")

    novo = Compra(nome_completo=nome_completo, email_1=email_1, telefone_1=telefone_1, mensagem=mensagem, valor_compra=valor_compra)
    db.session.add(novo)
    db.session.commit()

    return jsonify({"mensagem": "Compra enviada com sucesso!"})

@app.route("/finalizar_compra", methods=["POST"])
def finalizar_compra():
    nome = request.form.get("nome_completo")
    endereco = request.form.get("endereco")
    cpf = request.form.get("cpf")
    cep = request.form.get("cep")
    produtos = request.form.get("produtos")
    valor_total = float(request.form.get("valor_total"))

    nova = Compra(
        nome_completo=nome,
        endereco=endereco,
        cpf=cpf,
        cep=cep,
        produtos=produtos,
        valor_total=valor_total
    )
    db.session.add(nova)
    db.session.commit()
    return redirect(f"/relatorio/{nova.id}")

#rota compras nova
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
            "produtos": json.loads(c.produtos),
            "valor_total": c.valor_total
        })
    return jsonify(resultado)

@app.route("/relatorio/<int:id>")
def relatorio(id):
    compra = Compra.query.get_or_404(id)
    produtos = json.loads(compra.produtos)
    return render_template("relatorio.html", compra=compra, produtos=produtos)
