import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage
import sqlite3
import webbrowser
import os
from fpdf import FPDF
import matplotlib.pyplot as plt


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
        self.cursor.execute(
            "INSERT INTO tbl_usuarios (nome, telefone, email, usuario, senha, cidade) VALUES (?, ?, ?, ?, ?, ?)",
            (nome, telefone, email, usuario, senha, cidade))
        self.conn.commit()

    def update_user(self, idusuario, nome, telefone, email, usuario, senha, cidade):
        self.cursor.execute(
            "UPDATE tbl_usuarios SET nome=?, telefone=?, email=?, usuario=?, senha=?, cidade=? WHERE idusuario=?",
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


# Função para gerar e salvar PDF com todos os usuários e um gráfico
def gerar_pdf_usuarios():
    banco = Banco()
    banco.cursor.execute('SELECT * FROM tbl_usuarios')
    usuarios = banco.cursor.fetchall()

    if not usuarios:
        messagebox.showinfo("Informação", "Não há usuários cadastrados.")
        return

    # Criar um gráfico com a contagem de usuários por cidade
    cidades = [usuario[6] for usuario in usuarios]  # Considera a cidade do usuário
    contagem_cidades = {cidade: cidades.count(cidade) for cidade in set(cidades)}  # Contagem por cidade

    plt.figure(figsize=(10, 5))
    plt.bar(contagem_cidades.keys(), contagem_cidades.values())
    plt.xlabel('Cidades')
    plt.ylabel('Número de Usuários')
    plt.title('Número de Usuários por Cidade')
    plt.xticks(rotation=45)

    # Salvar o gráfico como imagem
    caminho_grafico = 'grafico_usuarios.png'
    plt.savefig(caminho_grafico)
    plt.close()  # Fechar a figura

    # Criar um objeto PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Adicionar dados dos usuários ao PDF
    for usuario in usuarios:
        pdf.cell(200, 10,
                 txt=f"ID: {usuario[0]}, Nome: {usuario[1]}, Telefone: {usuario[2]}, Email: {usuario[3]}, Usuário: {usuario[4]}, Cidade: {usuario[6]}",
                 ln=True)

    # Adicionar a imagem do gráfico ao PDF
    pdf.image(caminho_grafico, x=10, y=pdf.get_y() + 10, w=190)  # Ajustar posição e largura

    # Salvar o PDF como relatorio.pdf
    caminho_do_pdf = os.path.abspath('relatorio.pdf')
    pdf.output(caminho_do_pdf)

    # Abrir a nova janela de visualização de PDF
    VisualizarPDF(caminho_do_pdf)


# Classe para a janela de visualização do PDF
class VisualizarPDF:
    def __init__(self, caminho_do_pdf):
        self.window = tk.Toplevel()  # Criar uma nova janela
        self.window.title("Visualizar PDF")
        self.window.geometry("400x200")

        # Botão para escolher o arquivo PDF
        tk.Button(self.window, text="Selecionar PDF", command=lambda: self.selecionar_pdf(caminho_do_pdf)).pack(pady=20)

        # Botão para voltar
        tk.Button(self.window, text="Voltar", command=self.window.destroy).pack(pady=20)

    def selecionar_pdf(self, caminho_do_pdf):
        # Abre um diálogo para o usuário escolher o arquivo PDF
        arquivo_pdf = filedialog.askopenfilename(title="Selecione o arquivo PDF",
                                                 initialdir=os.path.dirname(caminho_do_pdf),
                                                 filetypes=[("PDF Files", "*.pdf")])

        if not arquivo_pdf:
            return  # Se o usuário cancelar, não faça nada

        if not os.path.exists(arquivo_pdf):
            messagebox.showerror("Erro", "Arquivo PDF não encontrado.")
            return

        try:
            webbrowser.open(f'file://{arquivo_pdf}')  # Abrir o PDF no navegador
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o PDF: {e}")


# Classe para a janela de adicionar/alterar usuários
class UsuarioForm:
    def __init__(self, master, usuario=None):
        self.master = master
        self.master.title("Adicionar/Alterar Usuário")
        self.master.geometry("300x300")

        self.banco = Banco()

        self.usuario = usuario
        if self.usuario:
            self.idusuario = self.usuario[0]  # Captura o ID do usuário se for edição
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
        self.entry_nome = tk.Entry(self.master)
        self.entry_nome.pack(pady=5)
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
        usuario_text = self.entry_usuario.get()
        senha = self.entry_senha.get()
        cidade = self.entry_cidade.get()

        if not all([nome, telefone, email, usuario_text, senha, cidade]):
            messagebox.showwarning("Advertência", "Todos os campos devem ser preenchidos.")
            return

        self.banco.add_user(nome, telefone, email, usuario_text, senha, cidade)
        messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso.")
        self.master.destroy()

    def alterar_usuario(self):
        nome = self.entry_nome.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()
        usuario_text = self.entry_usuario.get()
        senha = self.entry_senha.get()
        cidade = self.entry_cidade.get()

        if not all([nome, telefone, email, usuario_text, senha, cidade]):
            messagebox.showwarning("Advertência", "Todos os campos devem ser preenchidos.")
            return

        self.banco.update_user(self.idusuario, nome, telefone, email, usuario_text, senha, cidade)
        messagebox.showinfo("Sucesso", "Usuário alterado com sucesso.")
        self.master.destroy()


# Classe para a página principal
class PaginaPrincipal:
    def __init__(self, master):
        self.master = master
        self.master.title("Página Principal")
        self.master.geometry("500x500")

        self.frame_top = tk.Frame(self.master)
        self.frame_top.pack(pady=10)

        tk.Button(self.frame_top, text="Adicionar Usuário", command=self.adicionar_usuario).pack(pady=10, padx=5,
                                                                                                 side=tk.LEFT)
        tk.Button(self.frame_top, text="Alterar Usuário", command=self.alterar_usuario).pack(pady=10, padx=5,
                                                                                             side=tk.LEFT)
        tk.Button(self.frame_top, text="Excluir Usuário", command=self.excluir_usuario).pack(pady=10, padx=5,
                                                                                             side=tk.LEFT)
        tk.Button(self.frame_top, text="Gerenciar Usuários", command=self.gerenciar_usuarios).pack(pady=10, padx=5,
                                                                                                   side=tk.LEFT)
        tk.Button(self.frame_top, text="Visualizar PDF", command=gerar_pdf_usuarios).pack(pady=10, padx=5, side=tk.LEFT)

    def adicionar_usuario(self):
        UsuarioForm(tk.Toplevel())

    def alterar_usuario(self):
        usuario_selecionado = self.selecionar_usuario()
        if usuario_selecionado:
            UsuarioForm(tk.Toplevel(), usuario=usuario_selecionado)

    def excluir_usuario(self):
        usuario_selecionado = self.selecionar_usuario()
        if usuario_selecionado:
            if messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este usuário?"):
                banco = Banco()
                banco.delete_user(usuario_selecionado[0])
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso.")

    def gerenciar_usuarios(self):
        banco = Banco()
        usuarios = banco.get_all_users()

        if not usuarios:
            messagebox.showinfo("Gerenciar Usuários", "Não há usuários cadastrados.")
            return

        # Exibir todos os usuários em uma nova janela
        self.window = tk.Toplevel()
        self.window.title("Usuários Cadastrados")
        self.window.geometry("400x400")

        self.user_listbox = tk.Listbox(self.window)
        for usuario in usuarios:
            self.user_listbox.insert(tk.END, f"ID: {usuario[0]}, Nome: {usuario[1]}")
        self.user_listbox.pack(pady=10)

        tk.Button(self.window, text="Carregar Usuário", command=self.carregar_usuario).pack(pady=5)
        tk.Button(self.window, text="Voltar", command=self.window.destroy).pack(pady=5)

    def carregar_usuario(self):
        try:
            selection = self.user_listbox.curselection()
            if selection:
                index = selection[0]
                usuario_selecionado = self.user_listbox.get(index).split(",")[0].split(":")[1].strip()
                usuario = Banco().get_user_by_id(usuario_selecionado)
                if usuario:
                    UsuarioForm(tk.Toplevel(), usuario=usuario)
            else:
                messagebox.showwarning("Seleção", "Selecione um usuário para carregar.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao carregar o usuário: {e}")

    def selecionar_usuario(self):
        banco = Banco()
        usuarios = banco.get_all_users()
        if not usuarios:
            messagebox.showinfo("Selecionar Usuário", "Não há usuários cadastrados.")
            return None

        usuario_ids = [f"{usuario[0]} - {usuario[1]}" for usuario in usuarios]
        usuario_selecionado = tk.simpledialog.askstring("Selecionar Usuário",
                                                        "Digite o ID do usuário desejado:\n" + "\n".join(usuario_ids))

        if usuario_selecionado:
            try:
                idusuario = int(usuario_selecionado.split(" - ")[0])
                return banco.get_user_by_id(idusuario)
            except ValueError:
                messagebox.showwarning("Erro", "ID inválido.")


# Função para verificar login
def verificar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    # Verifique se as credenciais estão corretas
    if usuario == "admin" and senha == "1234":
        root.destroy()
        PaginaPrincipal(tk.Tk())  # Instancia a página principal
    else:
        messagebox.showerror("Login", "Usuário ou senha incorretos.")


# Criar a janela de login
root = tk.Tk()
root.title("Tela de Login")

# Adicionar um frame para organizar os widgets
frame = tk.Frame(root)
frame.pack(padx=20, pady=20, expand=True)

# Adicionar a imagem ao topo do frame
try:
    img = PhotoImage(file="imagens/buuuce.png")  # Caminho para a imagem
    lbimg = tk.Label(frame, image=img)
    lbimg.pack(pady=(0, 20))  # Adiciona padding abaixo da imagem
except Exception as e:
    print(f"Erro ao carregar a imagem: {e}")

# Adicionar rótulo e campos de entrada ao frame
tk.Label(frame, text="Usuário:").pack(pady=(10, 0))
entry_usuario = tk.Entry(frame)
entry_usuario.pack(pady=(5, 10))

tk.Label(frame, text="Senha:").pack(pady=(10, 0))
entry_senha = tk.Entry(frame, show="*")
entry_senha.pack(pady=(5, 10))

tk.Button(frame, text="Login", command=verificar_login).pack(pady=20)

# Configurar o tamanho da janela
root.geometry("720x600")

# Executar o loop principal
root.mainloop()
