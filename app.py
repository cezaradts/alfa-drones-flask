
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mensagens.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'chave_secreta'

db = SQLAlchemy(app)

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    mensagem = db.Column(db.Text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    mensagem = request.form['mensagem']

    nova_mensagem = Mensagem(nome=nome, email=email, telefone=telefone, mensagem=mensagem)
    db.session.add(nova_mensagem)
    db.session.commit()
    flash('Mensagem enviada com sucesso!')
    return redirect('/')

if __name__ == '__main__':
    if not os.path.exists('mensagens.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
