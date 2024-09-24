import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

# Classe para a página principal após o login
class PaginaPrincipal:
    def __init__(self, master):
        self.master = master
        self.master.title("Página Principal")
        self.master.geometry("400x300")

        self.banco = Banco()

        # Botões
        self.frame_botoes = tk.Frame(master)
        self.frame_botoes.pack(pady=20)

        self.btn_excluir = tk.Button(self.frame_botoes, text="Excluir", command=self.abrirExcluir)
        self.btn_excluir.pack(padx=5, pady=5)

        self.btn_alterar = tk.Button(self.frame_botoes, text="Alterar", command=self.abrirAlterar)
        self.btn_alterar.pack(padx=5, pady=5)

        self.btn_gerenciar = tk.Button(self.frame_botoes, text="Gerenciar", command=self.abrirGerenciar)
        self.btn_gerenciar.pack(padx=5, pady=5)

        self.btn_voltar = tk.Button(self.frame_botoes, text="Voltar", command=self.voltarLogin)
        self.btn_voltar.pack(pady=20)

    def abrirExcluir(self):
        ExcluirUsuario(self.master)

    def abrirAlterar(self):
        AlterarUsuario(self.master)

    def abrirGerenciar(self):
        GerenciarUsuarios(self.master)

    def voltarLogin(self):
        self.master.destroy()
        importar_login()

# Classe para excluir usuário
class ExcluirUsuario:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Excluir Usuário")
        self.master.geometry("400x300")

        self.banco = Banco()

        tk.Label(self.master, text="Selecione o usuário para excluir:").pack(pady=10)
        self.lista_usuarios = tk.Listbox(self.master, width=50)
        self.lista_usuarios.pack(pady=10)

        self.carregarUsuarios()

        tk.Button(self.master, text="Excluir", command=self.excluirUsuario).pack(pady=5)
        tk.Button(self.master, text="Voltar", command=self.master.destroy).pack(pady=5)

    def carregarUsuarios(self):
        usuarios = Usuarios().getAllUsers()
        for usuario in usuarios:
            self.lista_usuarios.insert(tk.END, f"ID: {usuario[0]} | Nome: {usuario[1]}")

    def excluirUsuario(self):
        selecao = self.lista_usuarios.curselection()
        if selecao:
            usuario_id = Usuarios().getAllUsers()[selecao[0]][0]
            Usuarios().idusuario = usuario_id
            msg = Usuarios().deleteUser()
            messagebox.showinfo("Resultado", msg)
            self.lista_usuarios.delete(selecao)
        else:
            messagebox.showwarning("Seleção", "Nenhum usuário selecionado.")

# Classe para alterar usuário
class AlterarUsuario:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Alterar Usuário")
        self.master.geometry("400x400")

        self.banco = Banco()

        tk.Label(self.master, text="ID do Usuário para Alterar:").pack(pady=10)
        self.entry_id = tk.Entry(self.master)
        self.entry_id.pack(pady=10)

        tk.Button(self.master, text="Buscar", command=self.buscarUsuario).pack(pady=5)

        self.frame_dados = tk.Frame(self.master)
        self.frame_dados.pack(pady=10)

        self.campos = {}
        for texto in ["Nome", "Telefone", "Email", "Usuário", "Senha", "Cidade"]:
            tk.Label(self.frame_dados, text=texto).grid(row=len(self.campos), column=0, padx=5, pady=5, sticky=tk.E)
            entry = tk.Entry(self.frame_dados)
            entry.grid(row=len(self.campos), column=1, padx=5, pady=5)
            self.campos[texto] = entry

        tk.Button(self.master, text="Alterar", command=self.alterarUsuario).pack(pady=5)
        tk.Button(self.master, text="Voltar", command=self.master.destroy).pack(pady=5)

    def buscarUsuario(self):
        user_id = self.entry_id.get()
        user = Usuarios()
        msg = user.selectUser(user_id)
        if msg == "Usuário não encontrado.":
            messagebox.showerror("Erro", msg)
            return

        self.campos["Nome"].delete(0, tk.END)
        self.campos["Nome"].insert(tk.END, user.nome)
        self.campos["Telefone"].delete(0, tk.END)
        self.campos["Telefone"].insert(tk.END, user.telefone)
        self.campos["Email"].delete(0, tk.END)
        self.campos["Email"].insert(tk.END, user.email)
        self.campos["Usuário"].delete(0, tk.END)
        self.campos["Usuário"].insert(tk.END, user.usuario)
        self.campos["Senha"].delete(0, tk.END)
        self.campos["Senha"].insert(tk.END, user.senha)
        self.campos["Cidade"].delete(0, tk.END)
        self.campos["Cidade"].insert(tk.END, user.cidade)

    def alterarUsuario(self):
        user = Usuarios()
        user.idusuario = self.entry_id.get()
        user.nome = self.campos["Nome"].get()
        user.telefone = self.campos["Telefone"].get()
        user.email = self.campos["Email"].get()
        user.usuario = self.campos["Usuário"].get()
        user.senha = self.campos["Senha"].get()
        user.cidade = self.campos["Cidade"].get()
        msg = user.updateUser()
        messagebox.showinfo("Resultado", msg)

# Classe para gerenciar usuários
class GerenciarUsuarios:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Gerenciar Usuários")
        self.master.geometry("600x400")

        self.banco = Banco()

        tk.Label(self.master, text="Lista de Usuários:").pack(pady=10)
        self.lista_usuarios = tk.Listbox(self.master, width=80, height=20)
        self.lista_usuarios.pack(pady=10)

        self.carregarUsuarios()

        tk.Button(self.master, text="Voltar", command=self.master.destroy).pack(pady=5)

    def carregarUsuarios(self):
        usuarios = Usuarios().getAllUsers()
        for usuario in usuarios:
            self.lista_usuarios.insert(tk.END, f"ID: {usuario[0]} | Nome: {usuario[1]} | Telefone: {usuario[2]} | Email: {usuario[3]} | Cidade: {usuario[6]}")

# Função para abrir a página principal após o login
def importar_login():
    root = tk.Tk()
    PaginaPrincipal(root)
    root.mainloop()
