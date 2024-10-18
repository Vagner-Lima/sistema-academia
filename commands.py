def adicionar_aluno(cursor, db, alunoinfo):
    comando = ("""INSERT INTO alunos
               (primeiroNome, ultimoNome, email, telefone, cpf, plano, datamatricula)
               VALUES (%(primeiroNome)s, %(ultimoNome)s, %(email)s, %(telefone)s, %(cpf)s, %(plano)s, %(datamatricula)s)""")
    # Executa o comando SQL com os valores fornecidos
    cursor.execute(comando, alunoinfo)
    db.commit()  # Salva as informações na database
    cursor.close() #Colocar no final do codigo!!! fecha a conexao do cursor
    db.close() #Colocar no final do codigo!!! fecha a conexao com a database
    print("Aluno adicionado com sucesso!")

def create_table(cursor, db):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos(
        ID int PRIMARY KEY AUTO_INCREMENT not NULL,
        primeiroNome varchar(255) not NULL,
        ultimoNome varchar(255) not NULL,
        email varchar(255) not NULL,
        telefone varchar(15),
        cpf varchar(15) not NULL,
        plano varchar(255),
        datamatricula date
    );""")
    db.commit()  # Salva as informações na database
    cursor.close() #Colocar no final do codigo!!! fecha a conexao do cursor
    db.close() #Colocar no final do codigo!!! fecha a conexao com a database