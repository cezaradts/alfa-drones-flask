
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

# Modelo
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    mensagem = db.Column(db.Text)

#zerar lista de contatos (tirar # da frente das 3 proximas linhas)
# with app.app_context():
  #  db.drop_all()
   # db.create_all()

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
    
    # comando para gerar tabela de contatos
from flask import Flask, render_template
import sqlite3  # ou seu banco de dados atual

app = Flask(__name__)

@app.route('/contatos-tabela')
def contatos_tabela():
    # Acesso ao banco ou sua lógica de obtenção dos dados
    conn = sqlite3.connect('seu_banco.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome, email, mensagem FROM contatos")
    dados = cursor.fetchall()
    conn.close()
    
    return render_template("tabela.html", contatos=dados)

if __name__ == "__main__":
    app.run(debug=True)
