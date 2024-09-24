import tkinter as tk
from tkinter import messagebox
from pagina_principal import PaginaPrincipal

def verificar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if usuario == "admin" and senha == "1234":
        root.destroy()
        root_principal = tk.Tk()
        PaginaPrincipal(root_principal)
        root_principal.mainloop()
    else:
        messagebox.showerror("Login", "Usuário ou senha incorretos.")

root = tk.Tk()
root.title("Tela de Login")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20, expand=True)

try:
    img = tk.PhotoImage(file="imagem/curinga.png")
    lbimg = tk.Label(frame, image=img)
    lbimg.pack(pady=(0, 20))
except Exception as e:
    print(f"Erro ao carregar a imagem: {e}")

tk.Label(frame, text="Usuário:").pack(pady=(10, 0))
entry_usuario = tk.Entry(frame)
entry_usuario.pack(pady=(5, 10))

tk.Label(frame, text="Senha:").pack(pady=(10, 0))
entry_senha = tk.Entry(frame, show="*")
entry_senha.pack(pady=(5, 10))

tk.Button(frame, text="Login", command=verificar_login).pack(pady=20)

root.geometry("300x300")
root.mainloop()
