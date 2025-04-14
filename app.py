from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from flask import send_file
import pandas as pd
import io
from models import Contato  # ou o nome correto do seu modelo



app = Flask(__name__)
CORS(app)
#daqui
@app.route('/exportar-contatos')
def exportar_contatos():
    contatos = Contato.query.all()
    dados = [{
        'Nome': c.nome,
        'Email': c.email,
        'Telefone': c.telefone,
        'Mensagem': c.mensagem,
        'Data': c.data.strftime('%d/%m/%Y %H:%M') if c.data else ''
    } for c in contatos]

    df = pd.DataFrame(dados)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Contatos')

    output.seek(0)
    return send_file(output, download_name='contatos.xlsx', as_attachment=True)



#ate aqui


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

if __name__ == "__main__":
    app.run(debug=True)
