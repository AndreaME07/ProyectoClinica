import MySQLdb 
from werkzeug.security import generate_password_hash

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
    

    # Inserta roles
    cursor.execute("""INSERT INTO Rol (Nombre) VALUES ('Administrador')""")
    cursor.execute("""INSERT INTO Rol (Nombre) VALUES ('Medico')""")

    # Obtiene los IDs de los roles
    cursor.execute("""SELECT id FROM Rol WHERE Nombre = 'Administrador'""")
    id_admin = cursor.fetchone()[0]
    cursor.execute("""SELECT id FROM Rol WHERE Nombre = 'Medico'""")
    id_medico = cursor.fetchone()[0]

    # Inserta usuarios con los IDs de los roles
    contrasena = generate_password_hash('password123')
    cursor.execute("""INSERT INTO Usuario (RFC, Nombre, ApePaterno, ApeMaterno, CedulaProfesional, Correo, Contrasena, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", ('123456789', 'Admin', 'Admin', 'Admin', '123456789', 'admin@admin.com', contrasena, id_admin))
    cursor.execute("""INSERT INTO Usuario (RFC, Nombre, ApePaterno, ApeMaterno, CedulaProfesional, Correo, Contrasena, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", ('123456789', 'Medico', 'Medico', 'Medico', '1234567890', 'user@user.com', contrasena, id_medico))
    
    db.commit()
    cursor.close()
    db.close()

if __name__ == '__main__':
    seed()
