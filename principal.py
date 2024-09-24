import sqlite3

class Banco:
    def __init__(self):
        self.conn = sqlite3.connect('usuarios.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                telefone TEXT,
                email TEXT,
                usuario TEXT,
                senha TEXT,
                cidade TEXT
            )
        ''')
        self.conn.commit()

    def __del__(self):
        self.conn.close()

class Usuarios:
    def __init__(self):
        self.banco = Banco()
        self.idusuario = None
        self.nome = None
        self.telefone = None
        self.email = None
        self.usuario = None
        self.senha = None
        self.cidade = None

    def getAllUsers(self):
        self.banco.cursor.execute('SELECT * FROM usuarios')
        return self.banco.cursor.fetchall()

    def selectUser(self, user_id):
        self.banco.cursor.execute('SELECT * FROM usuarios WHERE id=?', (user_id,))
        user = self.banco.cursor.fetchone()
        if user:
            self.idusuario, self.nome, self.telefone, self.email, self.usuario, self.senha, self.cidade = user
            return user
        return "Usuário não encontrado."

    def updateUser(self):
        if self.idusuario:
            self.banco.cursor.execute('''
                UPDATE usuarios SET nome=?, telefone=?, email=?, usuario=?, senha=?, cidade=?
                WHERE id=?
            ''', (self.nome, self.telefone, self.email, self.usuario, self.senha, self.cidade, self.idusuario))
            self.banco.conn.commit()
            return "Usuário atualizado com sucesso."
        return "Usuário não encontrado."

    def deleteUser(self):
        if self.idusuario:
            self.banco.cursor.execute('DELETE FROM usuarios WHERE id=?', (self.idusuario,))
            self.banco.conn.commit()
            return "Usuário excluído com sucesso."
        return "Usuário não encontrado."
