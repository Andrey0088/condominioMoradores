import sqlite3
import tkinter as tk
from tkinter import messagebox, Toplevel, ttk

# Banco de Dados
def connect_db():
    return sqlite3.connect("condominio.db")

def criar_tabelas():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS moradores (
            nome TEXT,
            cpf TEXT PRIMARY KEY,
            apartamento TEXT,
            bloco TEXT,
            vaga TEXT,
            responsaveis TEXT
        )
    """)
    conn.commit()
    conn.close()

def adicionar_morador(nome, cpf, apartamento, bloco, vaga, responsaveis):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO moradores (nome, cpf, apartamento, bloco, vaga, responsaveis)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, cpf, apartamento, bloco, vaga, responsaveis))
    conn.commit()
    conn.close()

def listar_moradores(filtro_nome=None, filtro_bloco=None):
    conn = connect_db()
    cursor = conn.cursor()
    query = """
        SELECT m1.nome, m1.cpf, m1.apartamento, m1.bloco, m1.vaga, IFNULL(m2.nome, 'Nenhum') AS responsavel_nome
        FROM moradores m1
        LEFT JOIN moradores m2 ON m1.responsaveis = m2.cpf
        WHERE 1=1
    """
    params = []
    if filtro_nome:
        query += " AND m1.nome LIKE ?"
        params.append(f"%{filtro_nome}%")
    if filtro_bloco:
        query += " AND m1.bloco = ?"
        params.append(filtro_bloco)
    cursor.execute(query, params)
    moradores = cursor.fetchall()
    conn.close()
    return moradores

# Interface Gráfica
def exibir_moradores():
    def atualizar_lista():
        for row in tree.get_children():
            tree.delete(row)
        nome_filtro = entry_nome_filtro.get()
        bloco_filtro = combo_bloco_filtro.get()
        moradores = listar_moradores(nome_filtro, bloco_filtro)
        for morador in moradores:
            tree.insert("", "end", values=morador)

    def exibir_detalhes_morador(event):
        selected_item = tree.item(tree.selection())['values']
        if selected_item:
            detalhes_janela = Toplevel(root)
            detalhes_janela.title("Detalhes do Morador")
            detalhes_janela.geometry("400x300")
            detalhes_janela.configure(bg="#E6F7FF")
            
            tk.Label(detalhes_janela, text="Detalhes do Morador", font=("Helvetica", 16, "bold"), bg="#E6F7FF").pack(pady=10)
            tk.Label(detalhes_janela, text=f"Nome: {selected_item[0]}", font=("Helvetica", 12), bg="#E6F7FF").pack(pady=5)
            tk.Label(detalhes_janela, text=f"CPF: {selected_item[1]}", font=("Helvetica", 12), bg="#E6F7FF").pack(pady=5)
            tk.Label(detalhes_janela, text=f"Apartamento: {selected_item[2]}", font=("Helvetica", 12), bg="#E6F7FF").pack(pady=5)
            tk.Label(detalhes_janela, text=f"Bloco: {selected_item[3]}", font=("Helvetica", 12), bg="#E6F7FF").pack(pady=5)
            tk.Label(detalhes_janela, text=f"Vaga de Estacionamento: {selected_item[4]}", font=("Helvetica", 12), bg="#E6F7FF").pack(pady=5)
            tk.Label(detalhes_janela, text=f"Responsável: {selected_item[5]}", font=("Helvetica", 12), bg="#E6F7FF").pack(pady=5)

    # Nova Janela
    janela = Toplevel(root)
    janela.title("Todos os Moradores")
    janela.geometry("900x500")
    janela.configure(bg="#E6F7FF")

    tk.Label(janela, text="Buscar por Nome:", font=("Helvetica", 12), bg="#E6F7FF").grid(row=0, column=0, padx=10, pady=5)
    entry_nome_filtro = tk.Entry(janela, font=("Helvetica", 12))
    entry_nome_filtro.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(janela, text="Buscar por Bloco:", font=("Helvetica", 12), bg="#E6F7FF").grid(row=0, column=2, padx=10, pady=5)
    combo_bloco_filtro = ttk.Combobox(janela, values=["", "A", "B", "C", "D"], font=("Helvetica", 12))
    combo_bloco_filtro.grid(row=0, column=3, padx=10, pady=5)

    tk.Button(janela, text="Buscar", command=atualizar_lista, bg="#4CAF50", fg="white", font=("Helvetica", 12)).grid(row=0, column=4, padx=10, pady=5)

    # Tabela
    columns = ("Nome", "CPF", "Apartamento", "Bloco", "Vaga", "Responsáveis")
    tree = ttk.Treeview(janela, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

    # Bind para evento de clique
    tree.bind("<Double-1>", exibir_detalhes_morador)

    atualizar_lista()

# Janela Principal
root = tk.Tk()
root.title("Cadastro de Moradores e Dependentes")
root.geometry("1200x500")
root.configure(bg="#E6F7FF")

# Título
title_label = tk.Label(root, text="Cadastro de Moradores e Dependentes", font=("Helvetica", 18, "bold"), bg="#E6F7FF")
title_label.pack(pady=10)

# Formulário
frame_form = tk.Frame(root, bg="#E6F7FF", padx=20, pady=20)
frame_form.pack(fill="x", padx=10, pady=10)

tk.Label(frame_form, text="Nome:", font=("Helvetica", 14), bg="#E6F7FF").grid(row=0, column=0, padx=10, pady=5)
entry_nome = tk.Entry(frame_form, font=("Helvetica", 14))
entry_nome.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_form, text="CPF:", font=("Helvetica", 14), bg="#E6F7FF").grid(row=1, column=0, padx=10, pady=5)
entry_cpf = tk.Entry(frame_form, font=("Helvetica", 14))
entry_cpf.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Apartamento:", font=("Helvetica", 14), bg="#E6F7FF").grid(row=2, column=0, padx=10, pady=5)
entry_apartamento = tk.Entry(frame_form, font=("Helvetica", 14))
entry_apartamento.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Bloco:", font=("Helvetica", 14), bg="#E6F7FF").grid(row=3, column=0, padx=10, pady=5)
entry_bloco = tk.Entry(frame_form, font=("Helvetica", 14))
entry_bloco.grid(row=3, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Vaga de Estacionamento:", font=("Helvetica", 14), bg="#E6F7FF").grid(row=4, column=0, padx=10, pady=5)
entry_vaga = tk.Entry(frame_form, font=("Helvetica", 14))
entry_vaga.grid(row=4, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Responsáveis (CPF):", font=("Helvetica", 14), bg="#E6F7FF").grid(row=5, column=0, padx=10, pady=5)
entry_responsaveis = tk.Entry(frame_form, font=("Helvetica", 14))
entry_responsaveis.grid(row=5, column=1, padx=10, pady=5)

def adicionar():
    adicionar_morador(entry_nome.get(), entry_cpf.get(), entry_apartamento.get(), entry_bloco.get(), entry_vaga.get(), entry_responsaveis.get())
    messagebox.showinfo("Sucesso", "Morador adicionado com sucesso!")

botao_adicionar = tk.Button(frame_form, text="Adicionar Morador", command=adicionar, font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="white")
botao_adicionar.grid(row=6, column=0, columnspan=2, pady=15)

# Botão "Exibir Moradores"
botao_exibir = tk.Button(root, text="Exibir Todos os Moradores", command=exibir_moradores, font=("Helvetica", 14, "bold"), bg="#007BFF", fg="white")
botao_exibir.pack(pady=20)

criar_tabelas()
root.mainloop()
