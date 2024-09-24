import tkinter as tk
from tkinter import *
from tkinter import ttk
from usuarios import Usuarios


class SistemaGestao:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Sistema de Gestão")
        self.master.geometry("600x500")  # Ajuste a largura e altura conforme necessário

        self.janela = Frame(master)
        self.fontePadrao = ("Arial", "12")
        self.janela.pack(fill=BOTH, expand=True)

        self.titulo = Label(self.janela, text="Informe os dados")
        self.titulo["font"] = ("Arial", 20, "bold")
        self.titulo.pack(pady=20)

        self.janela_campos = Frame(self.janela)
        self.janela_campos.pack(pady=10)

        # Campos de entrada
        self.idUsuarioLabel = Label(self.janela_campos, text="ID Usuário:", font=self.fontePadrao)
        self.idUsuarioLabel.grid(row=0, column=0, padx=5, pady=5, sticky=E)
        self.idUsuario = Entry(self.janela_campos)
        self.idUsuario.grid(row=0, column=1, padx=5, pady=5)

        self.btn_buscar = Button(self.janela_campos, text="Buscar", font=self.fontePadrao, command=self.buscarUsuario)
        self.btn_buscar.grid(row=0, column=2, padx=5, pady=5)

        self.nomeLabel = Label(self.janela_campos, text="Nome:", font=self.fontePadrao)
        self.nomeLabel.grid(row=1, column=0, padx=5, pady=5, sticky=E)
        self.nome = Entry(self.janela_campos)
        self.nome.grid(row=1, column=1, padx=5, pady=5)

        self.telefoneLabel = Label(self.janela_campos, text="Telefone:", font=self.fontePadrao)
        self.telefoneLabel.grid(row=2, column=0, padx=5, pady=5, sticky=E)
        self.telefone = Entry(self.janela_campos)
        self.telefone.grid(row=2, column=1, padx=5, pady=5)

        self.emailLabel = Label(self.janela_campos, text="Email:", font=self.fontePadrao)
        self.emailLabel.grid(row=3, column=0, padx=5, pady=5, sticky=E)
        self.email = Entry(self.janela_campos)
        self.email.grid(row=3, column=1, padx=5, pady=5)

        self.usuarioLabel = Label(self.janela_campos, text="Usuário:", font=self.fontePadrao)
        self.usuarioLabel.grid(row=4, column=0, padx=5, pady=5, sticky=E)
        self.usuario = Entry(self.janela_campos)
        self.usuario.grid(row=4, column=1, padx=5, pady=5)

        self.senhaLabel = Label(self.janela_campos, text="Senha:", font=self.fontePadrao)
        self.senhaLabel.grid(row=5, column=0, padx=5, pady=5, sticky=E)
        self.senha = Entry(self.janela_campos, show="*")
        self.senha.grid(row=5, column=1, padx=5, pady=5)

        self.cidadeLabel = Label(self.janela_campos, text="Cidade:", font=self.fontePadrao)
        self.cidadeLabel.grid(row=6, column=0, padx=5, pady=5, sticky=E)
        self.cidade = Entry(self.janela_campos)
        self.cidade.grid(row=6, column=1, padx=5, pady=5)

        # Botões
        self.janela_botoes = Frame(self.janela)
        self.janela_botoes.pack(pady=20)

        self.btn_inserir = Button(self.janela_botoes, text="Inserir", font=self.fontePadrao, width=10,
                                  command=self.inserirUsuario)
        self.btn_inserir.grid(row=0, column=0, padx=5)

        self.btn_alterar = Button(self.janela_botoes, text="Alterar", font=self.fontePadrao, width=10,
                                  command=self.alterarUsuario)
        self.btn_alterar.grid(row=0, column=1, padx=5)

        self.btn_excluir = Button(self.janela_botoes, text="Excluir", font=self.fontePadrao, width=10,
                                  command=self.excluirUsuario)
        self.btn_excluir.grid(row=0, column=2, padx=5)

        self.lblmsg = Label(master, text="", font=self.fontePadrao)
        self.lblmsg.pack(pady=10)

        # Treeview para mostrar todos os usuários
        self.tree_frame = Frame(master)
        self.tree_frame.pack(fill=BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame,
                                 columns=("ID", "Nome", "Telefone", "Email", "Usuário", "Senha", "Cidade"),
                                 show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Usuário", text="Usuário")
        self.tree.heading("Senha", text="Senha")
        self.tree.heading("Cidade", text="Cidade")
        self.tree.pack(fill=BOTH, expand=True)

        self.update_treeview()  # Atualiza a Treeview com dados do banco

    def buscarUsuario(self):
        user = Usuarios()
        idusuario = self.idUsuario.get()
        mensagem = user.selectUser(idusuario)
        self.lblmsg["text"] = mensagem
        if user.idusuario:
            self.idUsuario.delete(0, END)
            self.idUsuario.insert(INSERT, user.idusuario)
            self.nome.delete(0, END)
            self.nome.insert(INSERT, user.nome)
            self.telefone.delete(0, END)
            self.telefone.insert(INSERT, user.telefone)
            self.email.delete(0, END)
            self.email.insert(INSERT, user.email)
            self.usuario.delete(0, END)
            self.usuario.insert(INSERT, user.usuario)
            self.senha.delete(0, END)
            self.senha.insert(INSERT, user.senha)
            self.cidade.delete(0, END)
            self.cidade.insert(INSERT, user.cidade)

    def inserirUsuario(self):
        user = Usuarios()
        user.nome = self.nome.get()
        user.telefone = self.telefone.get()
        user.email = self.email.get()
        user.usuario = self.usuario.get()
        user.senha = self.senha.get()
        user.cidade = self.cidade.get()
        self.lblmsg["text"] = user.insertUser()
        self.limparCampos()
        self.update_treeview()

    def alterarUsuario(self):
        user = Usuarios()
        user.idusuario = self.idUsuario.get()
        user.nome = self.nome.get()
        user.telefone = self.telefone.get()
        user.email = self.email.get()
        user.usuario = self.usuario.get()
        user.senha = self.senha.get()
        user.cidade = self.cidade.get()
        self.lblmsg["text"] = user.updateUser()
        self.limparCampos()
        self.update_treeview()

    def excluirUsuario(self):
        user = Usuarios()
        user.idusuario = self.idUsuario.get()
        self.lblmsg["text"] = user.deleteUser()
        self.limparCampos()
        self.update_treeview()

    def limparCampos(self):
        self.idUsuario.delete(0, END)
        self.nome.delete(0, END)
        self.telefone.delete(0, END)
        self.email.delete(0, END)
        self.usuario.delete(0, END)
        self.senha.delete(0, END)
        self.cidade.delete(0, END)

    def update_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        user = Usuarios()
        c = user.banco.get_connection().cursor()
        c.execute("SELECT * FROM tbl_usuarios")
        for row in c.fetchall():
            self.tree.insert("", "end", values=row)
        c.close()


root = Tk()
SistemaGestao(root)
root.mainloop()
