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

# Banco de dados para compras novo
class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    produtos = db.Column(db.String(500), nullable=False)
    valor_total = db.Column(db.Float, nullable=False)



#zerar lista de contatos (tirar # da frente das 3 proximas linhas)
# with app.app_context():
 # db.drop_all()
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

# Rota de Compras nova
@app.route("/finalizar_compra", methods=["POST"])
def finalizar_compra():
    nome = request.form["nome_completo"]
    endereco = request.form["endereco"]
    cpf = request.form["cpf"]
    cep = request.form["cep"]
    produtos = request.form.get("produtos")  # Deve ser um JSON.stringify no HTML
    valor_total = float(request.form.get("valor_total"))

    nova = Compra(
        nome_completo=nome,
        endereco=endereco,
        cpf=cpf,
        cep=cep,
        produtos=produtos,
        valor_total=valor_total
    )
    db.session.add(nova)
    db.session.commit()
    return redirect(f"/relatorio/{nova.id}")

# Rota exibir relatorio Nova

from flask import render_template

@app.route("/relatorio/<int:id>")
def relatorio(id):
    compra = Compra.query.get_or_404(id)
    produtos = json.loads(compra.produtos)
    return render_template("relatorio.html", compra=compra, produtos=produtos)
    
if __name__ == "__main__":
    app.run(debug=True)
    app.run(debug=True)
