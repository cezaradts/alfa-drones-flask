from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Banco de dados para contato
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    mensagem = db.Column(db.Text)

#zerar lista de contatos (tirar # da frente das 3 proximas linhas)
#with app.app_context():
 #  db.drop_all()
 #  db.create_all()

# Rota principal
@app.route("/")
def index():
    return jsonify({"mensagem": "API Alfa Drones Contato está funcionando!"})

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

    novo = Contato(nome=nome, email=email,telefone=telefone, mensagem=mensagem)
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
            "mensagem": c.mensagem
        })
    return jsonify(resultado)

# Finalizar a partir daqui

# Banco de dados para finalizar
class Compra(db.Modelo):
    ido = db.Column(db.Integer, primary_key=True)
    Nome_Completo = db.Column(db.String(100))
    CPF = db.Column(db.String(20))
    Endereço = db.Column(db.String(20))
    CEP = db.Column(db.String(20))

#zerar lista  (tirar # da frente das 3 proximas linhas)
#with app.app_context():
 #  db.drop_all()
 #  db.create_all()

# Rota principal
@app.route1("/")
def index():
    return jsonify({"mensagem": "API Alfa Drones Compra está funcionando!"})

# Rota de teste
@app.route1("/test")
def test():
    return jsonify({"status": "OK", "mensagem": "Rota de teste Compra funcionando perfeitamente!"})

# Rota de contato
@app.route1("/compra", methods=["POST"])
def compra():
    ido = request.get_json()
    Nome_Completo= dados.get("Nome_Completo")
    CPF = dados.get("CPF")
    Endereço = dados.get("Endereço")
    CEP = dados.get("CEP")

    novo = Compra (Nome_Completo=Nome_Completo, CPF=CPF,Endereço=Endereço, CEP=CEP)
    db.session.add(novo)
    db.session.commit()

    return jsonify({"mensagem": "Compra enviada com sucesso!"})

# Rota para ler dados da compra
@app.route("/compras", methods=["GET"])
def listar_compras():
    compras = Compra.query.all()
    resultados = []
    for c in compras:
        resultados.append({
            "ido": c.ido,
            "Nome_Completo": c.Nome_Completo,
            "CPF": c.CPF,
            "Endereço": c.Endereço,
            "CEP": c.CEP
        })
    return jsonify(resultados)
# Termina aqui

if __name__ == "__main__":
    app.run(debug=True)
    app.run(debug=True)
