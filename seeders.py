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

    contrasena = generate_password_hash('password123')
    cursor.execute("""INSERT INTO Usuario (RFC, Nombre, ApePaterno, ApeMaterno, CedulaProfesional, Correo, Contrasena, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", ('123456789', 'Admin', 'Admin', 'Admin', '123456789', 'admin@admin.com', contrasena, id_admin))
    cursor.execute("""INSERT INTO Usuario (RFC, Nombre, ApePaterno, ApeMaterno, CedulaProfesional, Correo, Contrasena, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", ('123456789', 'Medico', 'Medico', 'Medico', '1234567890', 'user@user.com', contrasena, id_medico))
    cursor.execute("""INSERT INTO Usuario (RFC, Nombre, ApePaterno, ApeMaterno, CedulaProfesional, Correo, Contrasena, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", ('123456789', 'Medico2', 'Medico2', 'Medico2', '1234567890', 'medico@medico.com', contrasena, id_medico))

  # Obtener IDs de los médicos
    cursor.execute("SELECT id FROM Usuario WHERE id_rol = (SELECT id FROM Rol WHERE Nombre = 'Medico')")
    medicos = cursor.fetchall()

    # Datos de los pacientes a insertar
    pacientes = [
        ("Juan", "Pérez", "López", "1980-05-15", 1),   # id_Sexo = 1 (Masculino)
        ("María", "Gómez", "Martínez", "1992-11-23", 2), # id_Sexo = 2 (Femenino)
        ("Carlos", "Hernández", "García", "1985-02-10", 1),
        ("Luisa", "Fernández", "Ruiz", "1990-07-30", 2),
        ("Miguel", "Sánchez", "Jiménez", "1988-12-12", 1)
    ]

    # Insertar 5 pacientes por cada médico
    for medico in medicos:
        for paciente in pacientes:
            cursor.execute("""
                INSERT INTO Paciente (Nombre, ApePaterno, ApeMaterno, FechaNam, id_Sexo, id_Medico)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (*paciente, medico[0]))

    
    db.commit()
    cursor.close()
    db.close()

if __name__ == '__main__':
    seed()
