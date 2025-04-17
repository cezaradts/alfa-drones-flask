from flask import Flask, jsonify, request, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

analisar a partir da qui para interar

ate aqui

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    mensagem = db.Column(db.Text)

# Novo modelo para registrar compras
class Compra(db.Model):
    id_compras = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    produtos = db.Column(db.String(500), nullable=False)  # JSON ou lista formatada
    valor_total = db.Column(db.Float, nullable=False)
    data_compra = db.Column(db.DateTime, default=datetime.utcnow)
    
    #nova classe produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100))
    preco = db.Column(db.Float)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contato_id = db.Column(db.Integer, db.ForeignKey('contato.id'))
    produtos = db.relationship('Produto', secondary='pedido_produto', backref='pedidos')
    valor_total = db.Column(db.Float)

# Criar banco de dados (executar uma vez)
with app.app_context():
    db.create_all()
# ----------------- Novas Rotas para Compras ------------------

@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    dados = request.form
    nova_compra = Compra(
        nome_completo=dados['nome_completo'],
        endereco=dados['endereco'],
        cpf=dados['cpf'],
        cep=dados['cep'],
        produtos=json.dumps(dados.getlist('produtos')),  # Converte lista de produtos em JSON
        valor_total=float(dados['total'])
    )
    db.session.add(nova_compra)
    db.session.commit()
    return redirect(url_for('relatorio', id_compra=nova_compra.id))
    

#zerar lista de contatos (tirar # da frente das 3 proximas linhas)
with app.app_context():
   db.drop_all()
   db.create_all()

# Rota principal
@app.route("/")
def index():
    return jsonify({"mensagem": "API Alfa Drones está funcionando!"})

#rota compras
from flask import render_template

@app.route('/compras')
def listar_compras():
    compras = Compra.query.all()  # Pega todas as compras do banco
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

    novo = Contato(nome=nome, email=email,telefone=telefone, mensagem=mensagem)
    db.session.add(novo)
    db.session.commit()

    return jsonify({"mensagem": "Contato enviado com sucesso!"})

#que  relatorio compras
@app.route("/relatorio_compras", methods=["GET"])
def relatorio_compras():
    pedidos = Pedido.query.all()
    relatorio = []
    for pedido in pedidos:
        contato = Contato.query.get(pedido.contato_id)
        produtos = [{'nome': p.nome, 'preco': p.preco} for p in pedido.produtos]
        relatorio.append({
            'nome_completo': contato.nome_completo,
            'endereco': contato.endereco,
            'cpf': contato.cpf,
            'cep': contato.cep,
            'produtos': produtos,
            'valor_total': pedido.valor_total
        })
    return jsonify(relatorio)

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

if __name__ == "__main__":
    app.run(debug=True)
    app.run(debug=True)
