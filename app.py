from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import smtplib
import pandas as pd
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo do banco de dados
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mensagem = db.Column(db.Text)

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para salvar o contato
@app.route('/contato', methods=['POST'])
def contato():
    dados = request.get_json()
    novo_contato = Contato(
        nome=dados['nome'],
        email=dados['email'],
        mensagem=dados['mensagem']
    )
    db.session.add(novo_contato)
    db.session.commit()
    return jsonify({'mensagem': 'Contato enviado com sucesso!'})

# Rota para exibir os contatos como tabela
@app.route('/contatos')
def contatos():
    contatos = Contato.query.all()
    return render_template('tabela.html', contatos=contatos)

# Rota para enviar os contatos por e-mail
@app.route('/enviar-email')
def enviar_email():
    try:
        enviar_contatos_por_email()
        return "E-mail enviado com sucesso!"
    except Exception as e:
        print("Erro ao enviar e-mail:", e)
        return "Erro ao enviar e-mail."

# Função para gerar e enviar o Excel por e-mail
def enviar_contatos_por_email():
    # Gera Excel a partir do banco SQLite
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query("SELECT nome, email, mensagem FROM contato", conn)
    df.to_excel("contatos.xlsx", index=False)
    conn.close()

    # Credenciais (recomenda-se usar variáveis de ambiente no Render)
    remetente = os.environ.get("cesaradts@gmail.com") 
    senha = os.environ.get("0407@1966Aa!")    
    destinatario = cezaradts@gmail.com  

    # Monta e-mail com anexo
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = "Contatos do site Alfa Drones"

    parte = MIMEBase('application', 'octet-stream')
    with open("contatos.xlsx", "rb") as file:
        parte.set_payload(file.read())
    encoders.encode_base64(parte)
    parte.add_header('Content-Disposition', 'attachment; filename="contatos.xlsx"')
    msg.attach(parte)

    # Envia via Gmail (SMTP com SSL)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(remetente, senha)
        server.send_message(msg)
