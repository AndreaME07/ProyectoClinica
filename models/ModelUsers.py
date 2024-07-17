from .entidades.User import User

class ModelUser:
    @classmethod
    def login(self, rfc, mysql):
        try:
            cursor = mysql.connection.cursor()
            sql = """SELECT id, RFC, Contrasena, Nombre, ApePaterno, ApeMaterno, CedulaProfesional, Correo, id_rol FROM Usuario WHERE RFC=%s"""
            cursor.execute(sql, (rfc,))
            row = cursor.fetchone()
            if row is not None:
                return User(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            else:
                return None
        except Exception as e:
            print(e)
            return None
    @classmethod
    def get_by_id(self, mysql, id):
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT id, RFC, Contrasena, Nombre, ApePaterno, ApeMaterno, CedulaProfesional, Correo, id_rol FROM Usuario WHERE id=%s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row != None:
                logged_user = User(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                return logged_user
        except Exception as e:
            print(e)
            return None