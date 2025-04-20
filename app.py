from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///alfa_drones.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo Contato
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    mensagem = db.Column(db.Text)

# Modelo Compra
class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    cep = db.Column(db.String(10), nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)

@app.route('/contatos', methods=['POST'])
def receber_contato():
    data = request.json
    novo_contato = Contato(
        nome=data['nome'],
        email=data['email'],
        telefone=data['telefone'],
        mensagem=data['mensagem']
    )
    db.session.add(novo_contato)
    db.session.commit()
    return jsonify({'mensagem': 'Contato recebido com sucesso'}), 201

@app.route('/compras', methods=['POST'])
def registrar_compra():
    data = request.json
    nova_compra = Compra(
        nome=data['nome'],
        cpf=data['cpf'],
        endereco=data['endereco'],
        cep=data['cep'],
        valor_total=data['valor_total'],
        forma_pagamento=data['forma_pagamento']
    )
    db.session.add(nova_compra)
    db.session.commit()
    return jsonify({'mensagem': 'Compra registrada com sucesso'}), 201

@app.route('/relatorio-compras', methods=['GET'])
def relatorio_compras():
    compras = Compra.query.all()
    resultado = []
    for compra in compras:
        resultado.append({
            'nome': compra.nome,
            'cpf': compra.cpf,
            'endereco': compra.endereco,
            'cep': compra.cep,
            'valor_total': compra.valor_total,
            'forma_pagamento': compra.forma_pagamento
        })
    return jsonify(resultado)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
