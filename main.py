from datetime import datetime
import mysql.connector;
import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from commands import adicionar_aluno, create_table

app = Flask(__name__)

load_dotenv() # Carrega o .env onde fica as variaveis locais

config = {
    "password": os.getenv("password"),
    "host": os.getenv("host"),
    "user": os.getenv("user"),
    "database": os.getenv("database") # Coleta as informacoes do .env para a conexao com a database
}
db = mysql.connector.connect(**config) # Conecta com a database SQL
cursor = db.cursor() # Cria um cursor. Necessario para CRUD
diaHJ = datetime.now().strftime('%Y-%m-%d')


@app.route("/")
def home():
    return render_template("index.html")

@app.route('/adicionar_aluno', methods=['GET','POST'])
def adicionar():
    db = mysql.connector.connect(**config) # Conecta com a database SQL
    cursor = db.cursor() # Cria um cursor. Necessario para CRUD
    if request.method == 'POST':
        alunoinfo = {
            'primeiroNome': request.form['primeiroNome'],
            'ultimoNome': request.form['ultimoNome'],
            'email': request.form['email'],
            'telefone': request.form['telefone'],
            'cpf': request.form['cpf'],
            'plano': request.form['plano'],
            'datamatricula': diaHJ
        }
        adicionar_aluno(cursor, db, alunoinfo)  # Chama a função do outro arquivo
        return redirect(url_for('home'))
    return render_template("adicionar_aluno.html")


if __name__ == '__main__':
    create_table(cursor,db)
    app.run(debug=True)