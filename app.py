from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Caminho para banco SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Contato
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20))
    assunto = db.Column(db.String(100))
    mensagem = db.Column(db.Text)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)

# Cria as tabelas se não existirem
with app.app_context():
    db.create_all()

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Painel de contatos
@app.route('/admin/contatos')
def admin_contatos():
    contatos = Contato.query.order_by(Contato.data_envio.desc()).all()
    return render_template('admin_contatos.html', contatos=contatos)

# Rodar localmente
if __name__ == '__main__':
    app.run(debug=True)


#antigo
#from flask import Flask, jsonify, request
#from flask_sqlalchemy import SQLAlchemy
#from flask_cors import CORS
#import os

#app = Flask(__name__)
#CORS(app)

# Caminho para banco SQLite
#basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)

# Modelo de Contato
#class Contato(db.Model):
 #   id = db.Column(db.Integer, primary_key=True)
  #  nome = db.Column(db.String(100), nullable=False)
   # email = db.Column(db.String(120), nullable=False)
  #  telefone = db.Column(db.String(20))
   # assunto = db.Column(db.String(100))
   # mensagem = db.Column(db.Text)
   # data_envio = db.Column(db.DateTime, default=datetime.utcnow)

#zerar lista de contatos (tirar # da frente das 3 proximas linhas)
# with app.app_context():
  #  db.drop_all()
   # db.create_all()

# Página inicial
#@app.route('/')
#def index():
 #   return render_template('index.html')

# Cria as tabelas se não existirem
#with app.app_context():
    db.create_all()

# Rota principal
#@app.route("/")
#def index():
 #   return jsonify({"mensagem": "API Alfa Drones está funcionando!"})

# Rota de teste
#@app.route("/test")
#def test():
  #  return jsonify({"status": "OK", "mensagem": "Rota de teste funcionando perfeitamente!"})

# Rota de contato
#@app.route("/contato", methods=["POST"])
#def contato():
#    dados = request.get_json()
  #  id = db.Column(db.Integer, primary_key=True)
  #  nome = db.Column(db.String(100), nullable=False)
  #  email = db.Column(db.String(120), nullable=False)
  #  telefone = db.Column(db.String(20))
  #  assunto = db.Column(db.String(100))
  #  mensagem = db.Column(db.Text)
  #  data_envio = db.Column(db.DateTime, default=datetime.utcnow)

 #   novo = Contato(nome=nome, email=email,telefone=telefone, mensagem=mensagem, assunto=assunto, data_envio=data_envio)
 #   db.session.add(novo)
 #   db.session.commit()

 #   return jsonify({"mensagem": "Contato enviado com sucesso!"})

# Rota para ler dados do contato
#@app.route("/contatos", methods=["GET"])
#def listar_contatos():
 #   contatos = Contato.query.all()
 #   resultado = []
  #  for c in contatos:
  #      resultado.append({
   #         "id": c.id,
  #          "nome": c.nome,
   #         "email": c.email,
    #        "telefone": c.telefone,
     #       "mensagem": c.mensagem,
    #        "assunto": c.assunto,
     #       "data_envio": c.data_envio
        })
   # return jsonify(resultado)

#if __name__ == "__main__":
#    app.run(debug=True)

