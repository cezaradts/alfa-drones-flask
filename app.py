
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
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

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100))
    cpf = db.Column(db.String(20))
    produto = db.Column(db.String(100))
    preco = db.Column(db.Float)
    data = db.Column(db.DateTime, default=datetime.utcnow)

#zerar lista de contatos (tirar # da frente das 3 proximas linhas)
#with app.app_context():
 #  db.drop_all()
 #  db.create_all()

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
            "mensagem": c.mensagem
             "nome_completo": c.nome_completo,
            "cpf": c.cpf,
            "endereco": c.endereco,
            "cep": c.cep
        })
    return jsonify(resultado)

@app.route('/comprar', methods=['POST'])
def comprar():
    dados = request.json
    nova_compra = Compra(
        nome_completo=dados['nome_completo'],
        cpf=dados['cpf'],
        produto=dados['produto'],
        preco=dados['preco']
    )
    db.session.add(nova_compra)
    db.session.commit()
    return jsonify({'mensagem': 'Compra registrada com sucesso!'})


@app.route('/relatorio_compras', methods=['GET'])
def relatorio_compras():
    compras = Compra.query.order_by(Compra.data.desc()).all()
    resultado = [{
        'nome_completo': c.nome_completo,
        'cpf': c.cpf,
        'produto': c.produto,
        'preco': c.preco,
        'data': c.data.strftime('%d/%m/%Y %H:%M')
    } for c in compras]
    return jsonify(resultado)
    
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
    app.run(debug=True)
