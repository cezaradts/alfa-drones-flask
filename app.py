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
#with app.app_context():
 #  db.drop_all()
 #  db.create_all()

# Rota principal
@app.route("/")
def index():
    return jsonify({"mensagem": "API Alfa Drones está funcionando!"})

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
