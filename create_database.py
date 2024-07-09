import MySQLdb
import os

def create_database():
    db = MySQLdb.connect(
        host="localhost",
        user= "root",
        passwd= "",
        unix_socket= "/opt/lampp/var/mysql/mysql.sock"
    )
    cursor = db.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS db_clinicamayo")

    db.select_db("db_clinicamayo")
    #Tabla de Sexo
    cursor.execute("""CREATE TABLE IF NOT EXISTS Sexo(
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   Nombre VARCHAR(100) NOT NULL,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                   )""")
        #Tabla de roles
    cursor.execute("""CREATE TABLE IF NOT EXISTS Rol(
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   Nombre VARCHAR(100) NOT NULL,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                   )""")
    #Tabla de Usuarios
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Usuario(
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   RFC VARCHAR(13) NOT NULL,
                   Nombre VARCHAR(100) NOT NULL,
                   ApePaterno VARCHAR(100) NOT NULL,
                   ApeMaterno VARCHAR(100) NOT NULL,
                   CedulaProfesional VARCHAR(20) NOT NULL,
                   Correo VARCHAR(100) NOT NULL,
                   Contrasena VARCHAR(100) NOT NULL,
                   id_rol INT,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                   FOREIGN KEY (id_rol) REFERENCES Rol(id)
                   )""")
    #Tabla de Pacientes
    cursor.execute("""CREATE TABLE IF NOT EXISTS Paciente(
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   Nombre VARCHAR(100) NOT NULL,
                   ApePaterno VARCHAR(100) NOT NULL,
                   ApeMaterno VARCHAR(100) NOT NULL,
                   FechaNam DATE NOT NULL,
                   id_Sexo INT,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                   FOREIGN KEY (id_Sexo) REFERENCES Sexo(id)
                   )""")
        #Tabla de Expediente
    cursor.execute("""CREATE TABLE IF NOT EXISTS Expediente(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    id_Paciente INT,
                    id_Medico INT,
                    EnfermedadC TEXT(600) NOT NULL,
                    Alergias TEXT(600) NOT NULL,
                    AntecedentesFam TEXT(600) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_Paciente) REFERENCES Paciente(id),
                    FOREIGN KEY (id_Medico) REFERENCES Usuario(id)
                    )""")
    #Tabla de citas
    cursor.execute("""CREATE TABLE IF NOT EXISTS Cita(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    id_expediente INT,
                    Peso FLOAT NOT NULL,
                    Altura FLOAT NOT NULL,
                    Temperatura FLOAT NOT NULL,
                    LatMinuto INT(3) NOT NULL,
                    SatOxi FLOAT NOT NULL,
                    Glucosa FLOAT NOT NULL,
                    Edad INT(3) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_expediente) REFERENCES Expediente(id)
                   )""")
    #Tabla Diagnostico 
    cursor.execute("""CREATE TABLE IF NOT EXISTS Diagnostico(
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   id_Cita INT,
                   Sintomas TEXT(600) NOT NULL,
                   Dx TEXT(600) NOT NULL,
                   Tratamiento TEXT(600) NOT NULL,
                   Estudios TEXT(600) NOT NULL,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                   FOREIGN KEY (id_Cita) REFERENCES Cita(id)
                   )""")
    #Tabla de Recetas
    cursor.execute("""CREATE TABLE IF NOT EXISTS Receta(
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   id_Cita INT,
                   DatosMedicos TEXT(600) NOT NULL,
                   PdfReecetas BLOB,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                   FOREIGN KEY (id_Cita) REFERENCES Cita(id)
                   )""")
    

    
    db.commit()
    cursor.close()
    db.close()

if __name__ == "__main__":
    create_database()
    print("Database created")