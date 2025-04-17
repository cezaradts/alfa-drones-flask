from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ----------------- Modelos ------------------

# Modelo atual para mensagens (já existente)
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    mensagem = db.Column(db.Text)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)

# Novo modelo para registrar compras
class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(20), nullable=False)
    produto = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

# ----------------- Rotas Existentes ------------------

@app.route('/contato', methods=['POST'])
def contato():
    dados = request.json
    novo_contato = Contato(
        nome=dados['nome'],
        email=dados['email'],
        telefone=dados['telefone'],
        mensagem=dados['mensagem']
    )
    db.session.add(novo_contato)
    db.session.commit()
    return jsonify({'mensagem': 'Mensagem enviada com sucesso!'})

@app.route('/listar_contatos', methods=['GET'])
def listar_contatos():
    contatos = Contato.query.order_by(Contato.data_envio.desc()).all()
    resultado = [{
        'nome': c.nome,
        'email': c.email,
        'telefone': c.telefone,
        'mensagem': c.mensagem,
        'data_envio': c.data_envio.strftime('%d/%m/%Y %H:%M')
    } for c in contatos]
    return jsonify(resultado)

# ----------------- Novas Rotas para Compras ------------------

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

# ----------------- Inicialização do Banco ------------------

with app.app_context():
    db.create_all()

# ----------------- Executar Aplicação ------------------

if __name__ == '__main__':
    app.run(debug=True)
