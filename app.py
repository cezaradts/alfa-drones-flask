
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    mensagem = db.Column(db.Text)

class Compra(db.Model):
    id_compras = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    produtos = db.Column(db.String(500), nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    data_compra = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# PÃ¡gina com o formulÃ¡rio de finalizaÃ§Ã£o
@app.route('/finalizar_compra', methods=['GET'])
def mostrar_formulario():
    return render_template('https://cezaradts.github.io/alfa-drones-flask/templates/finalizarCompra.html')

# Receber os dados da compra
@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    dados = request.form
    nova_compra = Compra(
        nome_completo=dados['nome_completo'],
        endereco=dados['endereco'],
        cpf=dados['cpf'],
        cep=dados['cep'],
        produtos=json.dumps(dados.getlist('produtos')),
        valor_total=float(dados['valor_total'])
    )
    db.session.add(nova_compra)
    db.session.commit()
    return redirect(url_for('relatorio', id_compra=nova_compra.id_compras))

# Visualizar uma compra
@app.route("/relatorio/<int:id_compra>")
def relatorio(id_compra):
    compra = Compra.query.get_or_404(id_compra)
    produtos = json.loads(compra.produtos)
    return render_template("relatorio.html", compra=compra, produtos=produtos)

# Rota principal da API
@app.route("/")
def index():
    return jsonify({"mensagem": "API Alfa Drones estÃ¡ funcionando!"})

# Rota para listar todas as compras
@app.route('/compras')
def listar_compras():
    compras = Compra.query.all()
    return render_template('compras.html', compras=compras)

# Rota de teste
@app.route("/test")
def test():
    return jsonify({"status": "OK", "mensagem": "Rota de teste funcionando perfeitamente!"})

# Rota de contato
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
    return jsonify({"mensagem": "Contato registrado com sucesso!"})
