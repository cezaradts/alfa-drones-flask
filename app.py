from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

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
