from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, RFC, contrasena, Nombre, ApePaterno, ApeMaterno, CedulaProfesional, Correo, id_rol):
        self.id = id
        self.RFC = RFC
        self.contrasena = contrasena
        self.Nombre = Nombre
        self.ApePaterno = ApePaterno
        self.ApeMaterno = ApeMaterno
        self.CedulaProfesional = CedulaProfesional
        self.Correo = Correo
        self.id_rol = id_rol
    
    @classmethod
    def check_password(cls, hashed_password, contrasena):
        return check_password_hash(hashed_password, contrasena)
    