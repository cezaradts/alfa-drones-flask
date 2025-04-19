
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

# Modelo para compras parte nova
class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(200))
    cep = db.Column(db.String(20))
    valor_total = db.Column(db.Float)

// final parte nova
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
    
# compra sucesso nova
@app.route('/compras', methods=['POST'])
def salvar_compra():
    data = request.get_json()
    nova_compra = Compra(
        nome=data['nome'],
        endereco=data['endereco'],
        cep=data['cep'],
        valor_total=data['valor_total']
    )
    db.session.add(nova_compra)
    db.session.commit()
    return jsonify({'mensagem': 'Compra registrada com sucesso'}), 201

//final parte nova

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

// nova rota relatorio compras

@app.route('/relatorio_compras')
def relatorio_compras():
    compras = Compra.query.all()
    relatorio = [
        {
            'nome': c.nome,
            'endereco': c.endereco,
            'cep': c.cep,
            'valor_total': c.valor_total
        }
        for c in compras
    ]
    return jsonify(relatorio)

//final relatorio
