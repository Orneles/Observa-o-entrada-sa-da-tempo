from tkinter import messagebox
import tkinter as tk
import sqlite3
from datetime import datetime

# Conexão com o banco
conexao = sqlite3.connect("apartamento.db")
cursor = conexao.cursor()

# Criar tabela
cursor.execute("""
CREATE TABLE IF NOT EXISTS visitas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_visitante TEXT NOT NULL,
    horario_entrada TEXT NOT NULL,
    tempo_permanencia TEXT
)
""")
conexao.commit()

# Função para registrar entrada

def registrar_entrada(nome):
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO visitas (nome_visitante, horario_entrada)
        VALUES (?, ?)
    """, (nome, horario))
    conexao.commit()
    print(f"Entrada registrada para {nome} às {horario}")

# Função para registrar saída


def registrar_saida(nome):
    horario_saida = datetime.now()

    cursor.execute("""
        SELECT id, horario_entrada FROM visitas
        WHERE nome_visitante = ? AND horario_saida IS NULL
    """, (nome,))

    visita = cursor.fetchone()

    if visita:
        id_visita, horario_entrada = visita
        horario_entrada = datetime.strptime(
            horario_entrada, "%Y-%m-%d %H:%M:%S")
        tempo = horario_saida - horario_entrada

        cursor.execute("""
            UPDATE visitas
            SET horario_saida = ?, tempo_permanencia = ?
            WHERE id = ?
        """, (
            horario_saida.strftime("%Y-%m-%d %H:%M:%S"),
            str(tempo),
            id_visita
        ))

        conexao.commit()
        print(f"Saída registrada. Tempo no apartamento: {tempo}")
    else:
        print("Nenhuma visita em aberto encontrada.")


# MENU SIMPLES
while True:
    print("\n1 - Registrar entrada")
    print("2 - Registrar saída")
    print("3 - Listar visitas")
    print("4 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome = input("Nome do visitante: ")
        registrar_entrada(nome)

    elif opcao == "2":
        nome = input("Nome do visitante: ")
        registrar_saida(nome)

    elif opcao == "3":
        cursor.execute("SELECT * FROM visitas")
        visitas = cursor.fetchall()
        for v in visitas:
            print(v)

    elif opcao == "4":
        break

    else:
        print("Opção inválida")

conexao.close()


def gerar_relatorio(mes):
    conexao = sqlite3.connect("apartamento.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT 
            nome_visitante,
            COUNT(*) AS total_visitas,
            SUM(
                (strftime('%s', horario_saida) - strftime('%s', horario_entrada))
            ) AS tempo_total
        FROM visitas
        WHERE strftime('%Y-%m', horario_entrada) = ?
        AND horario_saida IS NOT NULL
        GROUP BY nome_visitante
    """, (mes,))

    resultados = cursor.fetchall()
    conexao.close()

    print(f"\n📊 RELATÓRIO DO MÊS {mes}")
    for nome, visitas, tempo in resultados:
        horas = tempo // 3600
        minutos = (tempo % 3600) // 60
        print(f"{nome} | Visitas: {visitas} | Tempo total: {horas}h {minutos}min")


# Exemplo
gerar_relatorio("2026-01")


# Banco de dados
conexao = sqlite3.connect("apartamento.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS visitas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_visitante TEXT,
    horario_entrada TEXT,
    horario_saida TEXT,
    tempo_permanencia TEXT
)
""")
conexao.commit()

# Funções


def registrar_entrada():
    nome = entrada_nome.get()
    if nome == "":
        messagebox.showerror("Erro", "Digite o nome")
        return

    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO visitas (nome_visitante, horario_entrada) VALUES (?, ?)",
        (nome, horario)
    )
    conexao.commit()
    messagebox.showinfo("Sucesso", f"Entrada registrada para {nome}")


def registrar_saida():
    nome = entrada_nome.get()

    cursor.execute("""
        SELECT id, horario_entrada FROM visitas
        WHERE nome_visitante = ? AND horario_saida IS NULL
    """, (nome,))
    visita = cursor.fetchone()

    if visita:
        id_visita, entrada = visita
        saida = datetime.now()
        entrada = datetime.strptime(entrada, "%Y-%m-%d %H:%M:%S")
        tempo = saida - entrada

        cursor.execute("""
            UPDATE visitas
            SET horario_saida = ?, tempo_permanencia = ?
            WHERE id = ?
        """, (
            saida.strftime("%Y-%m-%d %H:%M:%S"),
            str(tempo),
            id_visita
        ))
        conexao.commit()
        messagebox.showinfo("Saída", f"Tempo no apartamento: {tempo}")
    else:
        messagebox.showwarning("Aviso", "Nenhuma visita aberta")


def gerar_relatorio():
    mes = entrada_mes.get()

    cursor.execute("""
        SELECT nome_visitante, COUNT(*)
        FROM visitas
        WHERE strftime('%Y-%m', horario_entrada) = ?
        GROUP BY nome_visitante
    """, (mes,))

    resultado = cursor.fetchall()
    texto.delete(1.0, tk.END)

    for nome, total in resultado:
        texto.insert(tk.END, f"{nome} - {total} visitas\n")


# Interface
janela = tk.Tk()
janela.title("Controle de Visitas - Apartamento")
janela.geometry("400x450")

tk.Label(janela, text="Nome do Visitante").pack()
entrada_nome = tk.Entry(janela)
entrada_nome.pack()

tk.Button(janela, text="Registrar Entrada",
          command=registrar_entrada).pack(pady=5)
tk.Button(janela, text="Registrar Saída", command=registrar_saida).pack(pady=5)

tk.Label(janela, text="Relatório Mensal (AAAA-MM)").pack(pady=10)
entrada_mes = tk.Entry(janela)
entrada_mes.pack()

tk.Button(janela, text="Gerar Relatório", command=gerar_relatorio).pack(pady=5)

texto = tk.Text(janela, height=10)
texto.pack()

janela.mainloop()
conexao.close()


conexao = sqlite3.connect("apartamento.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS moradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    apartamento TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS visitantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    documento TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS visitas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visitante_id INTEGER,
    morador_id INTEGER,
    horario_entrada TEXT,
    horario_saida TEXT,
    tempo_permanencia TEXT
)
""")

conexao.commit()
conexao.close()


def cadastrar_morador(nome, apartamento):
    cursor.execute(
        "INSERT INTO moradores (nome, apartamento) VALUES (?, ?)",
        (nome, apartamento)
    )
    conexao.commit()


def cadastrar_visitante(nome, documento):
    cursor.execute(
        "INSERT INTO visitantes (nome, documento) VALUES (?, ?)",
        (nome, documento)
    )
    conexao.commit()


def registrar_entrada(visitante_id, morador_id):
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO visitas (visitante_id, morador_id, horario_entrada)
        VALUES (?, ?, ?)
    """, (visitante_id, morador_id, horario))
    conexao.commit()


def registrar_saida(visita_id):
    cursor.execute("""
        SELECT horario_entrada FROM visitas
        WHERE id = ? AND horario_saida IS NULL
    """, (visita_id,))

    entrada = cursor.fetchone()

    if entrada:
        entrada = datetime.strptime(entrada[0], "%Y-%m-%d %H:%M:%S")
        saida = datetime.now()
        tempo = saida - entrada

        cursor.execute("""
            UPDATE visitas
            SET horario_saida = ?, tempo_permanencia = ?
            WHERE id = ?
        """, (
            saida.strftime("%Y-%m-%d %H:%M:%S"),
            str(tempo),
            visita_id
        ))
        conexao.commit()


