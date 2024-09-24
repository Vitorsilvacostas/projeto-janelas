import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import webbrowser
import os
from fpdf import FPDF


# Defina a classe Banco para gerenciar operações de banco de dados
class Banco:
    def __init__(self):
        self.conn = sqlite3.connect('usuarios.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tbl_usuarios (
            idusuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            telefone TEXT,
            email TEXT,
            usuario TEXT,
            senha TEXT,
            cidade TEXT
        )""")
        self.conn.commit()

    def __del__(self):
        self.conn.close()


# Função para gerar e salvar PDF com todos os usuários
def gerar_pdf_usuarios():
    banco = Banco()
    banco.cursor.execute('SELECT * FROM tbl_usuarios')
    usuarios = banco.cursor.fetchall()

    if not usuarios:
        messagebox.showinfo("Informação", "Não há usuários cadastrados.")
        return

    # Criar um objeto PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Adicionar dados dos usuários ao PDF
    for usuario in usuarios:
        pdf.cell(200, 10, txt=f"ID: {usuario[0]}, Nome: {usuario[1]}, Telefone: {usuario[2]}, Email: {usuario[3]}, Usuário: {usuario[4]}, Cidade: {usuario[6]}", ln=True)

    # Salvar o PDF como relatorio.pdf
    caminho_do_pdf = os.path.abspath('relatorio.pdf')
    pdf.output(caminho_do_pdf)

    # Exibir um diálogo para escolher o arquivo PDF gerado
    visualizar_pdf(caminho_do_pdf)


# Função para visualizar PDF
def visualizar_pdf(caminho_do_pdf):
    # Abre um diálogo para o usuário escolher o arquivo PDF
    arquivo_pdf = filedialog.askopenfilename(title="Selecione o arquivo PDF", filetypes=[("PDF Files", "*.pdf")])

    if not arquivo_pdf:
        return  # Se o usuário cancelar, não faça nada

    if not os.path.exists(arquivo_pdf):
        messagebox.showerror("Erro", "Arquivo PDF não encontrado.")
        return

    try:
        webbrowser.open(f'file://{arquivo_pdf}')  # Abrir o PDF no navegador
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível abrir o PDF: {e}")


# Página principal do sistema
class PaginaPrincipal:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Gestão")
        self.master.geometry("800x600")

        self.frame_top = tk.Frame(self.master)
        self.frame_top.pack(side=tk.TOP, fill=tk.X)

        self.frame_bottom = tk.Frame(self.master)
        self.frame_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        tk.Button(self.frame_top, text="Adicionar Usuário", command=self.adicionar_usuario).pack(pady=10, padx=5, side=tk.LEFT)
        tk.Button(self.frame_top, text="Alterar Usuário", command=self.alterar_usuario).pack(pady=10, padx=5, side=tk.LEFT)
        tk.Button(self.frame_top, text="Excluir Usuário", command=self.excluir_usuario).pack(pady=10, padx=5, side=tk.LEFT)
        tk.Button(self.frame_top, text="Gerenciar Usuários", command=self.gerenciar_usuarios).pack(pady=10, padx=5, side=tk.LEFT)
        tk.Button(self.frame_top, text="Visualizar PDF", command=gerar_pdf_usuarios).pack(pady=10, padx=5, side=tk.LEFT)

    def adicionar_usuario(self):
        # Aqui você deve definir a lógica para adicionar um usuário
        messagebox.showinfo("Adicionar Usuário", "Função não implementada.")

    def alterar_usuario(self):
        # Aqui você deve definir a lógica para alterar um usuário
        messagebox.showinfo("Alterar Usuário", "Função não implementada.")

    def excluir_usuario(self):
        # Aqui você deve definir a lógica para excluir um usuário
        messagebox.showinfo("Excluir Usuário", "Função não implementada.")

    def gerenciar_usuarios(self):
        # Aqui você deve definir a lógica para gerenciar usuários
        messagebox.showinfo("Gerenciar Usuários", "Função não implementada.")


# Inicialização da aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = PaginaPrincipal(root)
    root.mainloop()
