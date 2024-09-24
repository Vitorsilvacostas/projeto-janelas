import tkinter as tk
from tkinter import ttk, messagebox, filedialog, PhotoImage
import sqlite3
import webbrowser
import os
from fpdf import FPDF


# Classe para gerenciar o banco de dados
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

    def add_user(self, nome, telefone, email, usuario, senha, cidade):
        self.cursor.execute("INSERT INTO tbl_usuarios (nome, telefone, email, usuario, senha, cidade) VALUES (?, ?, ?, ?, ?, ?)",
                            (nome, telefone, email, usuario, senha, cidade))
        self.conn.commit()

    def update_user(self, idusuario, nome, telefone, email, usuario, senha, cidade):
        self.cursor.execute("UPDATE tbl_usuarios SET nome=?, telefone=?, email=?, usuario=?, senha=?, cidade=? WHERE idusuario=?",
                            (nome, telefone, email, usuario, senha, cidade, idusuario))
        self.conn.commit()

    def delete_user(self, idusuario):
        self.cursor.execute("DELETE FROM tbl_usuarios WHERE idusuario=?", (idusuario,))
        self.conn.commit()

    def get_all_users(self):
        self.cursor.execute('SELECT * FROM tbl_usuarios')
        return self.cursor.fetchall()

    def get_user_by_id(self, idusuario):
        self.cursor.execute("SELECT * FROM tbl_usuarios WHERE idusuario=?", (idusuario,))
        return self.cursor.fetchone()


# Função para gerar e salvar PDF com todos os usuários
def gerar_pdf_usuarios():
    banco = Banco()
    banco.cursor.execute('SELECT * FROM tbl_usuarios')
    usuarios = banco.cursor.fetchall()

    if not usuarios:
        messagebox.showinfo("Informação", "Não há usuários cadastrados.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for usuario in usuarios:
        pdf.cell(200, 10, txt=f"ID: {usuario[0]}, Nome: {usuario[1]}, Telefone: {usuario[2]}, Email: {usuario[3]}, Usuário: {usuario[4]}, Cidade: {usuario[6]}", ln=True)

    caminho_do_pdf = os.path.abspath('relatorio.pdf')
    pdf.output(caminho_do_pdf)

    VisualizarPDF(caminho_do_pdf)


class VisualizarPDF:
    def __init__(self, caminho_do_pdf):
        self.window = tk.Toplevel()
        self.window.title("Visualizar PDF")
        self.window.geometry("400x200")

        tk.Button(self.window, text="Selecionar PDF", command=lambda: self.selecionar_pdf(caminho_do_pdf)).pack(pady=20)
        tk.Button(self.window, text="Voltar", command=self.window.destroy).pack(pady=20)

    def selecionar_pdf(self, caminho_do_pdf):
        arquivo_pdf = filedialog.askopenfilename(title="Selecione o arquivo PDF", initialdir=os.path.dirname(caminho_do_pdf), filetypes=[("PDF Files", "*.pdf")])

        if not arquivo_pdf:
            return

        if not os.path.exists(arquivo_pdf):
            messagebox.showerror("Erro", "Arquivo PDF não encontrado.")
            return

        try:
            webbrowser.open(f'file://{arquivo_pdf}')
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o PDF: {e}")


class UsuarioForm:
    def __init__(self, master, usuario=None, atualizar_funcao=None):
        self.master = master
        self.master.title("Adicionar/Alterar Usuário")
        self.master.geometry("300x300")

        self.banco = Banco()
        self.atualizar_funcao = atualizar_funcao

        self.usuario = usuario
        if self.usuario:
            self.idusuario = self.usuario[0]
            self.nome = self.usuario[1]
            self.telefone = self.usuario[2]
            self.email = self.usuario[3]
            self.usuario_text = self.usuario[4]
            self.senha = self.usuario[5]
            self.cidade = self.usuario[6]
        else:
            self.idusuario = None
            self.nome = ""
            self.telefone = ""
            self.email = ""
            self.usuario_text = ""
            self.senha = ""
            self.cidade = ""

        self.criar_widgets()

    def criar_widgets(self):
        tk.Label(self.master, text="Nome:").pack(pady=5)
        nome_frame = tk.Frame(self.master)
        nome_frame.pack(pady=5)

        self.entry_nome = tk.Entry(nome_frame)
        self.entry_nome.pack(side=tk.LEFT, padx=5)
        self.entry_nome.insert(0, self.nome)

        tk.Label(self.master, text="Telefone:").pack(pady=5)
        self.entry_telefone = tk.Entry(self.master)
        self.entry_telefone.pack(pady=5)
        self.entry_telefone.insert(0, self.telefone)

        tk.Label(self.master, text="Email:").pack(pady=5)
        self.entry_email = tk.Entry(self.master)
        self.entry_email.pack(pady=5)
        self.entry_email.insert(0, self.email)

        tk.Label(self.master, text="Usuário:").pack(pady=5)
        self.entry_usuario = tk.Entry(self.master)
        self.entry_usuario.pack(pady=5)
        self.entry_usuario.insert(0, self.usuario_text)

        tk.Label(self.master, text="Senha:").pack(pady=5)
        self.entry_senha = tk.Entry(self.master, show="*")
        self.entry_senha.pack(pady=5)
        self.entry_senha.insert(0, self.senha)

        tk.Label(self.master, text="Cidade:").pack(pady=5)
        self.entry_cidade = tk.Entry(self.master)
        self.entry_cidade.pack(pady=5)
        self.entry_cidade.insert(0, self.cidade)

        if self.usuario:
            tk.Button(self.master, text="Alterar Usuário", command=self.alterar_usuario).pack(pady=20)
        else:
            tk.Button(self.master, text="Adicionar Usuário", command=self.adicionar_usuario).pack(pady=20)

        tk.Button(self.master, text="Voltar", command=self.master.destroy).pack(pady=5)

    def adicionar_usuario(self):
        nome = self.entry_nome.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        cidade = self.entry_cidade.get()

        if not all([nome, telefone, email, usuario, senha, cidade]):
            messagebox.showwarning("Advertência", "Todos os campos devem ser preenchidos.")
            return

        self.banco.add_user(nome, telefone, email, usuario, senha, cidade)
        messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso.")
        self.atualizar_funcao()
        self.master.destroy()

    def alterar_usuario(self):
        nome = self.entry_nome.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        cidade = self.entry_cidade.get()

        if not all([nome, telefone, email, usuario, senha, cidade]):
            messagebox.showwarning("Advertência", "Todos os campos devem ser preenchidos.")
            return

        self.banco.update_user(self.idusuario, nome, telefone, email, usuario, senha, cidade)
        messagebox.showinfo("Sucesso", "Usuário alterado com sucesso.")
        self.atualizar_funcao()
        self.master.destroy()


class PaginaPrincipal:
    def __init__(self, master):
        self.master = master
        self.master.title("Gerenciamento de Usuários")
        self.master.geometry("800x600")

        self.banco = Banco()

        self.frame_top = tk.Frame(self.master)
        self.frame_top.pack(side=tk.TOP, fill=tk.X)

        self.frame_bottom = tk.Frame(self.master)
        self.frame_bottom.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        tk.Button(self.frame_top, text="Adicionar Usuário", command=self.adicionar_usuario).pack(pady=10, padx=5, anchor="center")
        tk.Button(self.frame_top, text="Alterar Usuário", command=self.alterar_usuario).pack(pady=10, padx=5, anchor="center")
        tk.Button(self.frame_top, text="Excluir Usuário", command=self.excluir_usuario).pack(pady=10, padx=5, anchor="center")
        tk.Button(self.frame_top, text="Gerar PDF", command=gerar_pdf_usuarios).pack(pady=10, padx=5, anchor="center")

        self.tree = ttk.Treeview(self.frame_bottom, columns=("ID", "Nome", "Telefone", "Email", "Usuário", "Cidade"), show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Usuário", text="Usuário")
        self.tree.heading("Cidade", text="Cidade")

        self.exibir_usuarios()

    def exibir_usuarios(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for usuario in self.banco.get_all_users():
            self.tree.insert("", "end", values=usuario)

    def adicionar_usuario(self):
        UsuarioForm(tk.Toplevel(self.master), atualizar_funcao=self.exibir_usuarios)

    def alterar_usuario(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertência", "Selecione um usuário para alterar.")
            return

        item = self.tree.item(selected_item)
        usuario_id = item['values'][0]
        usuario = self.banco.get_user_by_id(usuario_id)
        UsuarioForm(tk.Toplevel(self.master), usuario=usuario, atualizar_funcao=self.exibir_usuarios)

    def excluir_usuario(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertência", "Selecione um usuário para excluir.")
            return

        item = self.tree.item(selected_item)
        usuario_id = item['values'][0]
        self.banco.delete_user(usuario_id)
        messagebox.showinfo("Sucesso", "Usuário excluído com sucesso.")
        self.exibir_usuarios()


if __name__ == "__main__":
    root = tk.Tk()
    app = PaginaPrincipal(root)
    root.mainloop()
