import MySQLdb

def seed():
    db = MySQLdb.connect(
        host="localhost",
        user= "root",
        passwd= "",
        unix_socket= "/opt/lampp/var/mysql/mysql.sock"
    )
    cursor = db.cursor()
    db.select_db("db_clinicamayo")

    #seeder de sexo
    cursor.execute("""INSERT INTO Sexo (Nombre) VALUES ('Masculino')""")
    cursor.execute("""INSERT INTO Sexo (Nombre) VALUES ('Femenino')""")
    

    #seeder de roles
    cursor.execute("""INSERT INTO Rol (Nombre) VALUES ('Administrador')""")
    cursor.execute("""INSERT INTO Rol (Nombre) VALUES ('Medico')""")

    #seeder de usuarios
    cursor.execute("""INSERT INTO Usuario (RFC, Nombre, ApePaterno, ApeMaterno, CedulaProfesional, Correo, Contrasena, id_rol) VALUES ('XAXX010101000', 'Admin','Admin','Admin','123456789', "admin@example.com", 'password123', 1)""")
    cursor.execute("""INSERT INTO Usuario (RFC, Nombre, ApePaterno, ApeMaterno, CedulaProfesional, Correo, Contrasena, id_rol) VALUES ('XAXX010101001', 'Medico','Medico','Medico','1234567890', 'user@example.com', 'password123', 2)""")

    db.commit()
    cursor.close()
    db.close()

if __name__ == '__main__':
    seed()
