import sqlite3
import datetime
import tkinter as tk 
from tkinter import messagebox
from PIL import Image, ImageTk

DATABASE = 'escola_musica.db'

#-------- FUNÇÕES DE BANCO DE DADOS --------#

def conectar_db():
    return sqlite3.connect(DATABASE)

def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS alunos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   telefone TEXT,
                   data_inicio TEXT NOT NULL,
                   curso TEXT NOT NULL
                      )
               ''')
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS mensalidades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                   aluno_id INTEGER NOT NULL,
                   mes_referencia TEXT NOT NULL,
                   data_pagamento TEXT,
                   valor REAL NOT NULL,
                   pago INTEGER NOT NULL,
                   FOREIGN KEY (aluno_id) REFERENCES alunos(id)
                   )
               ''')
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS progresso_alunos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                   aluno_id INTEGER NOT NULL,
                   data_registro TEXT NOT NULL,
                   observacao TEXT,
                   nivel_atual TEXT,
                   proxima_meta TEXT,
                   FOREIGN KEY (aluno_id) REFERENCES alunos(id)
                   )
         ''')       
    conexao.commit()
    conexao.close()

#------------ FUNÇÇOES DE LOGICA DO PROGRAMA (CHAMADAS PELA INTERFACE) -----------#

def cadastrar_aluno_db(nome, telefone, data_inicio, curso, valor_mensalidade):
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO alunos (nome, telefone, data_inicio, curso) VALUES (?, ?, ?, ?)",
                       (nome, telefone, data_inicio, curso))
        aluno_id = cursor.lastrowid

        mes_inicio = datetime.datetime.strptime(data_inicio, '%Y-%m-%d').strftime('%Y-%m')
        cursor.execute("INSERT INTO mensalidades (aluno_id, mes_referencia, valor, pago) VALUES (?, ?, ?, ?)",
                       (aluno_id, mes_inicio, valor_mensalidade, 0))
        conexao.commit()
        conexao.close()
        messagebox.showinfo("Sucesso", f"Aluno '{nome}' cadastrado com sucesso! ID: {aluno_id}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao cadastrar o aluno: {str(e)}")

def registrar_pagamento_db(aluno_id, mes_referencia, data_pagamento):
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("UPDATE mensalidades SET data_pagamento = ?, pago = 1 WHERE aluno_id = ? AND mes_referencia = ?",
                       (data_pagamento, aluno_id, mes_referencia))
        conexao.commit()
        conexao.close()
        messagebox.showinfo("Sucesso", "Pagamento registrado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao registrar o pagamento: {str(e)}")

def registrar_progresso_db(aluno_id, data_registro, observacao, nivel_atual, proxima_meta):
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO progresso_alunos (aluno_id, data_registro, observacao, nivel_atual, proxima_meta) VALUES (?, ?, ?, ?, ?)",
                       (aluno_id, data_registro, observacao, nivel_atual, proxima_meta))
        conexao.commit()
        conexao.close()
        messagebox.showinfo("Sucesso", "Progresso registrado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao registrar o progresso: {str(e)}")

