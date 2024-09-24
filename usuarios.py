from banco import Banco

class Usuarios:
    def __init__(self):
        self.banco = Banco()

    def getAllUsers(self):
        try:
            with self.banco.conn:
                self.banco.cursor.execute("SELECT * FROM tbl_usuarios")
                return self.banco.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao obter usuários: {e}")
            return []

    def deleteUser(self, usuario_id):
        try:
            with self.banco.conn:
                self.banco.cursor.execute("DELETE FROM tbl_usuarios WHERE idusuario = ?", (usuario_id,))
                self.banco.conn.commit()
                return "Usuário excluído com sucesso."
        except Exception as e:
            print(f"Erro ao excluir usuário: {e}")
            return "Erro ao excluir usuário."
