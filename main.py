from datetime import datetime
import mysql.connector;
import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for, flash
from commands import adicionar_aluno, create_table

app = Flask(__name__)
app.secret_key = "123123"

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
        flash('Aluno adicionado com sucesso!', 'success')
        return redirect(url_for('adicionar'))
    return render_template("adicionar_aluno.html")

@app.route('/ver_alunos')
def ver_alunos():
    db = mysql.connector.connect(**config) # Conecta com a database SQL
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, primeiroNome, ultimoNome, email, telefone, cpf, plano, datamatricula FROM alunos") # * nao constava o id
    alunos = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("ver_alunos.html", alunos = alunos)

@app.route('/remover_aluno/<int:aluno_id>', methods=["POST"])
def remover_aluno(aluno_id):
    db = mysql.connector.connect(**config) # Conecta com a database SQL
    cursor = db.cursor() # Cria um cursor. Necessario para CRUD
    try:
            # Comando SQL para deletar um aluno com base no ID
            cursor.execute("DELETE FROM alunos WHERE id = %s", (aluno_id,))
            db.commit()  # Salvar as alterações no banco de dados
            return redirect('/ver_alunos')  # Redirecionar para a lista de alunos após a remoção
    except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return "Erro ao remover o aluno"
    finally:
        cursor.close()
        db.close()

@app.route('/atualizar_aluno/<int:aluno_id>', methods=['GET', 'POST'])
def atualizar_aluno(aluno_id):
    db = mysql.connector.connect(**config) # Conecta com a database SQL
    cursor = db.cursor() # Cria um cursor. Necessario para CRUD
    if request.method == 'POST':
        aluno_info = {
            'primeiroNome': request.form['primeiroNome'],
            'ultimoNome': request.form['ultimoNome'],
            'email': request.form['email'],
            'telefone': request.form['telefone'],
            'cpf': request.form['cpf'],
            'plano': request.form['plano'],
            'datamatricula': request.form['datamatricula'],
            'id': aluno_id  # ID do aluno a ser atualizado
        }
        comando = """UPDATE alunos SET
                     primeiroNome = %(primeiroNome)s,
                     ultimoNome = %(ultimoNome)s,
                     email = %(email)s,
                     telefone = %(telefone)s,
                     cpf = %(cpf)s,
                     plano = %(plano)s,
                     datamatricula = %(datamatricula)s
                     WHERE id = %(id)s"""
        
        cursor.execute(comando, aluno_info)
        db.commit()
        cursor.close()
        db.close()
        
        flash('Aluno atualizado com sucesso!', 'success')
        return redirect(url_for('atualizar_aluno', aluno_id = aluno_id))

    # Carregar os dados do aluno
    cursor.execute("SELECT id, primeiroNome, ultimoNome, email, telefone, cpf, plano, datamatricula FROM alunos WHERE id = %s", (aluno_id,))
    aluno = cursor.fetchone()
    db.close()

    if aluno is None:
        flash('Aluno não encontrado!', 'danger')
        return redirect(url_for('ver_alunos'))

    # Converter a tupla para um dicionário
    aluno_data = {
        'id': aluno[0],
        'primeiroNome': aluno[1],
        'ultimoNome': aluno[2],
        'email': aluno[3],
        'telefone': aluno[4],
        'cpf': aluno[5],
        'plano': aluno[6],
        'datamatricula': aluno[7]
    }

    # Passar os dados do aluno para o template
    return render_template("atualizar_aluno.html", aluno=aluno_data)
if __name__ == '__main__':
    create_table(cursor,db)
    app.run(debug=True)