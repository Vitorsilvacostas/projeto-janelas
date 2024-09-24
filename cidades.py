import sqlite3
import tkinter as tk
from tkinter import ttk

# Classe para gerenciar o banco de dados
class Banco:
    def __init__(self):
        self.conexao = sqlite3.connect('banco.db')
        self.create_tables()

    def create_tables(self):
        c = self.conexao.cursor()

        # Tabela de cidades
        c.execute("""
            CREATE TABLE IF NOT EXISTS tbl_cidades (
                idcidade INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT
            )
        """)

        # Tabela de usuários
        c.execute("""
            CREATE TABLE IF NOT EXISTS tbl_usuarios (
                idusuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                telefone TEXT,
                email TEXT,
                usuario TEXT,
                senha TEXT,
                idcidade INTEGER,
                FOREIGN KEY (idcidade) REFERENCES tbl_cidades(idcidade)
            )
        """)

        self.conexao.commit()
        c.close()

    def close(self):
        self.conexao.close()

# Classe para manipular usuários
class Usuarios:
    def __init__(self, db):
        self.db = db

    def select_user(self, idusuario):
        c = self.db.conexao.cursor()
        c.execute("SELECT * FROM tbl_usuarios WHERE idusuario=?", (idusuario,))
        user = c.fetchone()
        c.execute("SELECT nome FROM tbl_cidades WHERE idcidade=?", (user[6],))
        cidade = c.fetchone()[0] if user[6] else "Não informado"
        c.close()

        if user:
            self.idusuario, self.nome, self.telefone, self.email, self.usuario, self.senha, self.idcidade = user
            return f"Usuário {idusuario} encontrado!"
        else:
            return "Usuário não encontrado!"

    def insert_user(self):
        c = self.db.conexao.cursor()
        c.execute("""
            INSERT INTO tbl_usuarios (nome, telefone, email, usuario, senha, idcidade)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.nome, self.telefone, self.email, self.usuario, self.senha, self.idcidade))
        self.db.conexao.commit()
        c.close()
        return "Usuário inserido com sucesso!"

    def update_user(self):
        c = self.db.conexao.cursor()
        c.execute("""
            UPDATE tbl_usuarios
            SET nome=?, telefone=?, email=?, usuario=?, senha=?, idcidade=?
            WHERE idusuario=?
        """, (self.nome, self.telefone, self.email, self.usuario, self.senha, self.idcidade, self.idusuario))
        self.db.conexao.commit()
        c.close()
        return "Usuário atualizado com sucesso!"

    def delete_user(self):
        c = self.db.conexao.cursor()
        c.execute("DELETE FROM tbl_usuarios WHERE idusuario=?", (self.idusuario,))
        self.db.conexao.commit()
        c.close()
        return "Usuário excluído com sucesso!"

# Classe para a interface gráfica
class SistemaGestao:
    def __init__(self, master=None):
        self.janela = tk.Frame(master)
        self.fontePadrao = ("Arial", "12")
        self.janela.pack()

        self.titulo = tk.Label(self.janela, text="Informe os dados")
        self.titulo["font"] = ("Arial", 20, "bold")
        self.titulo.pack(pady=20)

        self.janela_campos = tk.Frame(master)
        self.janela_campos.pack(pady=10)

        self.idUsuarioLabel = tk.Label(self.janela_campos, text="ID Usuário:", font=self.fontePadrao)
        self.idUsuarioLabel.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.idUsuario = tk.Entry(self.janela_campos)
        self.idUsuario.grid(row=0, column=1, padx=5, pady=5)

        self.btn_buscar = tk.Button(self.janela_campos, text="Buscar", font=self.fontePadrao, command=self.buscar_usuario)
        self.btn_buscar.grid(row=0, column=2, padx=5, pady=5)

        self.nomeLabel = tk.Label(self.janela_campos, text="Nome:", font=self.fontePadrao)
        self.nomeLabel.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.nome = tk.Entry(self.janela_campos)
        self.nome.grid(row=1, column=1, padx=5, pady=5)

        self.telefoneLabel = tk.Label(self.janela_campos, text="Telefone:", font=self.fontePadrao)
        self.telefoneLabel.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.telefone = tk.Entry(self.janela_campos)
        self.telefone.grid(row=2, column=1, padx=5, pady=5)

        self.emailLabel = tk.Label(self.janela_campos, text="Email:", font=self.fontePadrao)
        self.emailLabel.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.email = tk.Entry(self.janela_campos)
        self.email.grid(row=3, column=1, padx=5, pady=5)

        self.usuarioLabel = tk.Label(self.janela_campos, text="Usuário:", font=self.fontePadrao)
        self.usuarioLabel.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.usuario = tk.Entry(self.janela_campos)
        self.usuario.grid(row=4, column=1, padx=5, pady=5)

        self.senhaLabel = tk.Label(self.janela_campos, text="Senha:", font=self.fontePadrao)
        self.senhaLabel.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.senha = tk.Entry(self.janela_campos, show="*")
        self.senha.grid(row=5, column=1, padx=5, pady=5)

        self.cidadeLabel = tk.Label(self.janela_campos, text="Cidade:", font=self.fontePadrao)
        self.cidadeLabel.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.cidade = ttk.Combobox(self.janela_campos)
        self.cidade.grid(row=6, column=1, padx=5, pady=5)
        self.carregar_cidades()

        self.janela_botoes = tk.Frame(master)
        self.janela_botoes.pack(pady=20)

        self.btn_inserir = tk.Button(self.janela_botoes, text="Inserir", font=self.fontePadrao, width=10, command=self.inserir_usuario)
        self.btn_inserir.grid(row=0, column=0, padx=5)

        self.btn_alterar = tk.Button(self.janela_botoes, text="Alterar", font=self.fontePadrao, width=10, command=self.alterar_usuario)
        self.btn_alterar.grid(row=0, column=1, padx=5)

        self.btn_excluir = tk.Button(self.janela_botoes, text="Excluir", font=self.fontePadrao, width=10, command=self.excluir_usuario)
        self.btn_excluir.grid(row=0, column=2, padx=5)

        self.lblmsg = tk.Label(master, text="", font=self.fontePadrao)
        self.lblmsg.pack()

        self.db = Banco()  # Criação da instância do banco de dados
        self.usuario_model = Usuarios(self.db)

    def carregar_cidades(self):
        c = self.db.conexao.cursor()
        c.execute("SELECT idcidade, nome FROM tbl_cidades")
        cidades = c.fetchall()
        self.cidade["values"] = [cidade[1] for cidade in cidades]
        self.cidade_data = {cidade[1]: cidade[0] for cidade in cidades}
        c.close()

    def buscar_usuario(self):
        idusuario = self.idUsuario.get()
        self.lblmsg["text"] = self.usuario_model.select_user(idusuario)
        self.idUsuario.delete(0, tk.END)
        self.idUsuario.insert(tk.INSERT, self.usuario_model.idusuario)
        self.nome.delete(0, tk.END)
        self.nome.insert(tk.INSERT, self.usuario_model.nome)
        self.telefone.delete(0, tk.END)
        self.telefone.insert(tk.INSERT, self.usuario_model.telefone)
        self.email.delete(0, tk.END)
        self.email.insert(tk.INSERT, self.usuario_model.email)
        self.usuario.delete(0, tk.END)
        self.usuario.insert(tk.INSERT, self.usuario_model.usuario)
        self.senha.delete(0, tk.END)
        self.senha.insert(tk.INSERT, self.usuario_model.senha)
        if self.usuario_model.idcidade:
            self.cidade.set(self.usuario_model.idcidade)
        else:
            self.cidade.set("")

    def inserir_usuario(self):
        self.usuario_model.nome = self.nome.get()
        self.usuario_model.tele
