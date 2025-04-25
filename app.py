from flask import Flask, jsonify, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados no Render
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
    whatsapp = db.Column(db.String(20), nullable=False)
    mail = db.Column(db.String(100), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)
    itens = db.Column(db.Text, nullable=False)

with app.app_context():
    db.drop_all()
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
    novo = Contato(
        nome=dados.get("nome"),
        email=dados.get("email"),
        telefone=dados.get("telefone"),
        mensagem=dados.get("mensagem")
    )
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

@app.route("/compras", methods=["POST"])
def registrar_compra():
    dados = request.get_json()
    try:
        nova = Compra(
            nome_completo=dados.get("nome"),
            endereco=dados.get("endereco"),
            cpf=dados.get("cpf"),
            whatsapp=dados.get("whatsapp"),
            mail=dados.get("mail"),
            cep=dados.get("cep"),
            valor_total=dados.get("valor_total"),
            forma_pagamento=dados.get("forma_pagamento"),
            itens=dados.get("itens")
        )
        db.session.add(nova)
        db.session.commit()
        return jsonify({"mensagem": "Compra registrada com sucesso!", "id": nova.id}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

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
            "whatsapp": c.whatsapp,
            "mail": c.mail,
            "cep": c.cep,
            "valor_total": c.valor_total,
            "forma_pagamento": c.forma_pagamento,
            "itens": c.itens
        })
    return jsonify(resultado)

@app.route("/relatorio/<int:id>")
def relatorio(id):
    compra = Compra.query.get_or_404(id)
    return render_template("relatorio.html", compra=compra)

@app.route("/relatorio-compras")
def relatorio_compras():
    compras = Compra.query.all()
    return render_template("relatorio_todas_compras.html", compras=compras)

if __name__ == "__main__":
    app.run(debug=True)
