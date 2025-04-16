 <td>${contato.mensagem}</td>from flask import Flask, jsonify, request
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alfa_drones.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Banco de dados para contato
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    mensagem = db.Column(db.Text)
    nome_completo = db.Column(db.String(100))
    cpf = db.Column(db.String(20))
    endereco = db.Column(db.String(20))
    cep = db.Column(db.String(20))

#classe para compras
class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100))
    cpf = db.Column(db.String(20))
    produto = db.Column(db.String(100))  # nome do produto comprado
    preco = db.Column(db.Float)
    data = db.Column(db.DateTime, default=datetime.utcnow)
 
 #classe finalizar
class Finalizar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Nome_Completo = db.Column(db.String(100))
    CPF = db.Column(db.String(20))
    Endereço = db.Column(db.String(200))
    CEP = db.Column(db.String(20))
 

# Rota principal
@app.route("/")
def index():
    return jsonify({"mensagem": "API Alfa Drones Contato esta funcionando!"})

# Rota de teste
@app.route("/test")
def test():
    return jsonify({"status": "OK", "mensagem": "Rota de teste Contato funcionando perfeitamente!"})

# Rota de contato
@app.route("/contato", methods=["POST"])
def contato():
    dados = request.get_json()
    nome = dados.get("nome")
    email = dados.get("email")
    telefone = dados.get("telefone")
    mensagem = dados.get("mensagem")
    nome_completo= dados.get("nome_completo")
    cpf = dados.get("cpf")
    endereco = dados.get("endereco")
    cep = dados.get("CEP")

    novo = Contato(nome=nome, email=email,telefone=telefone, mensagem=mensagem, nome_completo=nome_completo, cpf=cpf, endereco=endereco, CEP=CEP)
    db.session.add(novo)
    db.session.commit()

    return jsonify({"mensagem": "Contato enviado com sucesso!"})

# Rota para ler dados do contato
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
            "mensagem": c.mensagem,
             "nome_completo": c.nome_completo,
            "cpf": c.cpf,
            "endereco": c.endereco,
            "cep": c.cep
        })
    return jsonify(resultado)
@app.route("/finalizar", methods=["POST"])
def finalizar():
    dados = request.get_json()
    nome = dados.get("Nome_Completo")
    cpf = dados.get("CPF")
    endereco = dados.get("Endereço")
    cep = dados.get("CEP")
    
    novo = Finalizar(Nome_Completo=nome, CPF=cpf, Endereço=endereco, CEP=cep)
    db.session.add(novo)
    db.session.commit()
    
    return jsonify({"mensagem": "Compra finalizada com sucesso!"})

@app.route("/relatorio_compras", methods=["GET"])
def relatorio_compras():
    compradores = Finalizar.query.all()
    resultado = []
    for c in compradores:
        resultado.append({
            "Nome_Completo": c.Nome_Completo,
            "CPF": c.CPF,
            "Endereço": c.Endereço,
            "CEP": c.CEP
        })
    return jsonify(resultado)

#rota de compras
from datetime import datetime

@app.route("/comprar", methods=["POST"])
def comprar():
    dados = request.get_json()
    compra = Compra(
        nome_completo=dados.get("nome_completo"),
        cpf=dados.get("cpf"),
        produto=dados.get("produto"),
        preco=dados.get("preco")
    )
    db.session.add(compra)
    db.session.commit()
    return jsonify({"mensagem": "Compra registrada com sucesso!"})

#rota relatorio
@app.route("/relatorio_compras", methods=["GET"])
def relatorio_compras():
    compras = Compra.query.all()
    resultado = []
    for c in compras:
        resultado.append({
            "nome_completo": c.nome_completo,
            "cpf": c.cpf,
            "produto": c.produto,
            "preco": c.preco,
            "data": c.data.strftime('%d/%m/%Y %H:%M')
        })
    return jsonify(resultado)

#criar uma compra
POST /comprar
Content-Type: application/json

{
  "nome_completo": "Carlos da Silva",
  "cpf": "123.456.789-00",
  "produto": "Drone Note 14 Pro Plus",
  "preco": 3599.99
}

#zerar lista de contatos (tirar # da frente das 3 proximas linhas)
with app.app_context():
   db.drop_all()
  db.create_all()
 
if __name__ == "__main__":
    app.run(debug=True)
    app.run(debug=True)
