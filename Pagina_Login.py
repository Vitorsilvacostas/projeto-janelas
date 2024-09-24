import tkinter as tk
from tkinter import messagebox, PhotoImage
import pagina_principal

def verificar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    # Verifique se as credenciais estão corretas
    if usuario == "admin" and senha == "1234":
        root.destroy()
        pagina_principal.PaginaPrincipal(tk.Tk())  # Instancia a página principal
    else:
        messagebox.showerror("Login", "Usuário ou senha incorretos.")

# Criar a janela principal
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
