from datetime import datetime
import mysql.connector;
import os
from dotenv import load_dotenv

load_dotenv() # Carrega o .env onde fica as variaveis locais

config = {
    "password": os.getenv("password"),
    "host": os.getenv("host"),
    "user": os.getenv("user"),
    "database": os.getenv("database") # Coleta as informacoes do .env para a conexao com a database
}

connect = mysql.connector.connect(**config) # Conecta com a database SQL

cursor = connect.cursor() # Cria um cursor. Necessario para CRUD

diaHJ = datetime.now().date()

def adicionarAluno():  # Função para adicionar um novo aluno na database
    comando = ("""
    INSERT INTO alunos
    (primeiroNome, ultimoNome, email, telefone, cpf, plano, datamatricula)
    VALUES (%(primeiroNome)s, %(ultimoNome)s, %(email)s, %(telefone)s, %(cpf)s, %(plano)s, %(datamatricula)s)
    """)  # Comando SQL para adicionar o aluno
    
    # Coletar os dados do aluno e colocá-los em um dicionário
    alunoinfo = {
        'primeiroNome': input("Insira seu primeiro nome: "),
        'ultimoNome': input("Insira seu último nome: "),
        'email': input("Insira seu email: "),
        'telefone': input("Insira seu telefone: "),
        'cpf': input("Insira seu CPF: "),
        'plano': input("Insira o plano escolhido: "),
        'datamatricula': diaHJ
    }
    
    # Executa o comando SQL com os valores fornecidos
    cursor.execute(comando, alunoinfo)
    connect.commit()  # Salva as informações na database
    
    print("Aluno adicionado com sucesso!")
adicionarAluno()

cursor.close() #Colocar no final do codigo!!! fecha a conexao do cursor
connect.close() #Colocar no final do codigo!!! fecha a conexao com a database
