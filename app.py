from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_mysqldb import MySQL
from create_database import create_database
from functools import wraps
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
# Modelos
from models.ModelUsers import ModelUser

# Entidades
from models.entidades.User import User

# Decorador Roles
def roles_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'id' not in session:
                return redirect(url_for('accesoLogin'))
            user_role_id = session.get('id_rol')
            
            # Convertir el ID de rol a nombre de rol
            cur = mysql.connection.cursor()
            cur.execute('SELECT Nombre FROM Rol WHERE id = %s', [user_role_id])
            result = cur.fetchone()
            if result:
                user_role_name = result[0]
            else:
                user_role_name = None
            cur.close()
            
            print(f"User role: {user_role_name}, Allowed roles: {allowed_roles}")
            if user_role_name not in allowed_roles:
                flash('No tienes permiso para acceder a esta página', 'error')
                return redirect(url_for('menuPaciente')) 
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

app = Flask(__name__, template_folder='template')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_clinicamayo'
app.config['MYSQL_UNIX_SOCKET'] = '/opt/lampp/var/mysql/mysql.sock'  
app.config['SESION_PERMANENT']= False
app.secret_key = 'mysecretkey'

mysql = MySQL(app)
login_manager_app = LoginManager(app)
csrf = CSRFProtect()
create_database()

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(mysql, id)

@app.route('/')
def home():
    return render_template('index.html')

# Función de login
@app.route('/accesoLogin', methods=["GET", "POST"])
def accesoLogin():
    if request.method == 'POST':
        rfc = request.form['txtrfc']
        password = request.form['txtpassword']
        
        logged_user = ModelUser.login(rfc, mysql)
        if logged_user is not None:
            if User.check_password(logged_user.contrasena, password):
                session['id'] = logged_user.id
                session['id_rol'] = logged_user.id_rol
                
                login_user(logged_user)
                return redirect(url_for('menu'))
            else:
                flash('Contraseña incorrecta')
                return render_template('index.html')
        else:
            flash('Usuario no encontrado')
            return render_template('index.html')
    return render_template('index.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('accesoLogin'))

@app.route('/menu')
@login_required
@roles_required(['Administrador']) 
def menu():
    cur = mysql.connection.cursor()
    cur.execute('SELECT Usuario.*, Rol.Nombre FROM Usuario JOIN Rol ON Usuario.id_Rol = Rol.id')
    usuario = cur.fetchall()
    return render_template('admin_menu.html', usuario=usuario)

# Funciones de crud Medico
@app.route('/editarMedico/<id>')
@login_required
@roles_required(['Administrador'])
def editarMedico(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Usuario WHERE id = %s', [id])
    usuario = cur.fetchall()
    cur.execute('SELECT * FROM Rol')
    roles = cur.fetchall()
    return render_template('editarMedico.html', usuario=usuario, roles=roles)

@app.route('/actualizarMedico/<id>', methods=['POST'])
@login_required
@roles_required(['Administrador'])
def actualizarMedico(id):
    if request.method == 'POST':
        nombre = request.form['txtNombre']
        apellidoPa = request.form['txtApePaterno']
        apellidoMa = request.form['txtApeMaterno']
        rfc = request.form['txtRFC']
        cedula = request.form['txtCedula']
        correo = request.form['txtCorreo']
        contrasena = request.form['txtContrasena']
        rol = request.form['txtRol']

        hashed_contrasena = generate_password_hash(contrasena)

        cur = mysql.connection.cursor()
        cur.execute("UPDATE Usuario SET Nombre = %s, ApePaterno = %s, ApeMaterno = %s, RFC = %s, CedulaProfesional = %s, Correo = %s, Contrasena = %s, id_Rol = %s WHERE id = %s", (nombre, apellidoPa, apellidoMa, rfc, cedula, correo,hashed_contrasena, rol, id))
        mysql.connection.commit()
        flash('Usuario actualizado correctamente')
        return redirect(url_for('menu'))

@app.route('/buscarMedico', methods=['POST'])
@login_required
@roles_required(['Administrador'])
def buscarMedico():
    if request.method == 'POST':
        medico = request.form['buscarMedico']
        cur = mysql.connection.cursor()
        cur.execute('SELECT Usuario.*, Rol.Nombre FROM Usuario JOIN Rol ON Usuario.id_Rol = Rol.id WHERE Usuario.Nombre LIKE %s', ['%' + medico + '%'])
        if cur.rowcount > 0:
            usuario = cur.fetchall()
            return render_template('admin_menu.html', usuario=usuario)
        else:
            flash('No se encontró el médico')
            cur.execute('SELECT Usuario.*, Rol.Nombre FROM Usuario JOIN Rol ON Usuario.id_Rol = Rol.id')
            usuario = cur.fetchall()

        return render_template('admin_menu.html', usuario=usuario)

    return render_template('buscarMedico.html')

@app.route('/eliminarMedico/<id>')
@login_required
@roles_required(['Administrador'])
def eliminarMedico(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Usuario WHERE id = %s', [id])
    mysql.connection.commit()
    flash('Usuario eliminado correctamente')
    return redirect(url_for('menu'))

@app.route('/altaMedico')
@login_required
@roles_required(['Administrador'])
def agregarMedico():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Rol')
    roles = cur.fetchall()
    return render_template('agregarMedico.html', roles=roles)

@app.route('/guardarMedico', methods=["POST"])
@login_required
@roles_required(['Administrador'])
def guardarMedico():
    if request.method == 'POST' and 'txtNombre' in request.form and 'txtApePaterno' in request.form and 'txtApeMaterno' in request.form and 'txtRFC' in request.form and 'txtCedula' in request.form and 'txtCorreo' in request.form and 'txtContrasena' in request.form and 'txtRol' in request.form:
        fnombre = request.form['txtNombre']
        fapepaterno = request.form['txtApePaterno']
        fapematerno = request.form['txtApeMaterno']
        frfc = request.form['txtRFC']
        fcedula = request.form['txtCedula']
        fcorreo = request.form['txtCorreo']
        fcontrasena = request.form['txtContrasena']
        frol = request.form['txtRol']

        hashed_contrasena = generate_password_hash(fcontrasena)

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Usuario (Nombre, ApePaterno, ApeMaterno, RFC, CedulaProfesional, Correo, Contrasena, id_Rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (fnombre, fapepaterno, fapematerno, frfc, fcedula, fcorreo, hashed_contrasena, frol))
        mysql.connection.commit()
        cursor.close()
        
        flash('Médico agregado correctamente', 'success')
        return redirect(url_for('menu'))
    else:
        flash('Error al agregar médico', 'error')
        return redirect(url_for('home'))
######################################################
# Funciones de crud Paciente
@app.route('/menuPaciente')
@login_required
@roles_required(['Administrador', 'Medico'])
def menuPaciente():
    cur = mysql.connection.cursor()
    if session['id_rol'] == 1:
        cur.execute('''
            SELECT Paciente.*, Usuario.*, Rol.Nombre
            FROM Paciente 
            JOIN Usuario ON Paciente.id_Medico = Usuario.id
            JOIN Rol ON Usuario.id_Rol = Rol.id
        ''')
        paciente = cur.fetchall()
        
    else:
        cur.execute('SELECT * FROM Paciente WHERE id_Medico = %s', [current_user.id])
        paciente = cur.fetchall()
    return render_template('admin_user.html', paciente=paciente)

@app.route('/buscarPaciente', methods=['POST'])
@login_required
@roles_required(['Administrador', 'Medico'])
def buscarPaciente():
    if request.method == 'POST':
        paciente = request.form['buscarPaciente']
        cur = mysql.connection.cursor()
        if session['id_rol'] == 1:
            cur.execute('''
                SELECT Paciente.*, Usuario.*, Rol.Nombre
                FROM Paciente 
                JOIN Usuario ON Paciente.id_Medico = Usuario.id
                JOIN Rol ON Usuario.id_Rol = Rol.id
                WHERE Paciente.Nombre LIKE %s
            ''', ['%' + paciente + '%'])
        else:
            cur.execute('SELECT * FROM Paciente WHERE Nombre LIKE %s AND id_Medico = %s', ['%' + paciente + '%', current_user.id])
        if cur.rowcount > 0:
            paciente = cur.fetchall()
            return render_template('admin_user.html', paciente=paciente)
        else:
            flash('No se encontró el paciente')
            if session['id_rol'] == 1:
                cur.execute('''
                    SELECT Paciente.*, Usuario.*, Rol.Nombre
                    FROM Paciente 
                    JOIN Usuario ON Paciente.id_Medico = Usuario.id
                    JOIN Rol ON Usuario.id_Rol = Rol.id
                ''')
                paciente = cur.fetchall()
            else:
                cur.execute('SELECT * FROM Paciente WHERE id_Medico = %s', [current_user.id])
                paciente = cur.fetchall()

        return render_template('admin_user.html', paciente=paciente)

    return render_template('buscarPaciente.html')

@app.route('/diagnosticoPaciente')
def diagnosticoPaciente():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Paciente')
    paciente = cur.fetchall()
    return render_template('diagnostico.html', paciente=paciente)


@app.route('/diagnostico')
def diagnostico():
    return render_template('diagnostico.html')

@app.route('/citaExploracion/<id>')
@login_required
@roles_required(['Administrador', 'Medico'])
def citaExploracion(id):
    cur = mysql.connection.cursor()

    # Consulta de Paciente
    cur.execute('SELECT * FROM Paciente WHERE id = %s', [id])
    paciente = cur.fetchone()

    # Consulta de Expediente
    expediente = None
    if paciente:
        cur.execute('SELECT * FROM Expediente WHERE id_Paciente = %s', [id])
        expediente = cur.fetchone()

    # Consulta de Cita
    cita = None
    if expediente:
        cur.execute('SELECT * FROM Cita WHERE id_expediente = %s', [expediente['id']])
        cita = cur.fetchone()

    # Consulta de Receta
    receta = None
    if cita:
        cur.execute('SELECT * FROM Receta WHERE id_cita = %s', [cita['id']])
        receta = cur.fetchone()

    return render_template('citaPaciente.html', paciente=paciente, expediente=expediente, cita=cita, receta=receta)


@app.route('/expedientePaciente/<id>')
@login_required
@roles_required(['Administrador', 'Medico'])
def expedientePaciente(id):
    cur = mysql.connection.cursor()

    cur.execute('''
        SELECT Paciente.*, Expediente.* 
        FROM Paciente 
        LEFT JOIN Expediente ON Paciente.id = Expediente.id_Paciente 
        WHERE Paciente.id = %s
    ''', [id])
    
    paciente = cur.fetchall()

    if len(paciente) == 0 or paciente[0][len(paciente[0])-1] is None:
        cur.execute('SELECT * FROM Paciente WHERE id = %s', [id])
        paciente = cur.fetchall()
        
        user_id = current_user.id  
        return render_template('crearExpediente.html', paciente=paciente, user_id=user_id)
    
    return render_template('expediente.html', paciente=paciente)



@app.route('/crearExpediente/<id>')
@login_required
@roles_required(['Administrador', 'Medico'])
def crearExpediente(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Paciente WHERE id = %s', [id])
    paciente = cur.fetchall()
    return render_template('crearExpediente.html', paciente=paciente)

@app.route('/guardarExpediente', methods=["POST"])
@login_required
@roles_required(['Administrador', 'Medico'])
def guardarExpediente():
    if request.method == 'POST' and 'id_medico' in request.form and 'id_paciente' in request.form and 'enfCro' in request.form and 'alergias' in request.form and 'antFam' in request.form and 'created_by' in request.form:
        fid_paciente = request.form['id_paciente']
        fid_medico = request.form['id_medico']
        fenfCro = request.form['enfCro']
        falergias = request.form['alergias']
        fantFam = request.form['antFam']
        fcreated_by = request.form['created_by']

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Expediente (id_Paciente, id_Medico, EnfermedadC, Alergias, AntecedentesFam, created_by) VALUES (%s, %s, %s, %s, %s, %s)', (fid_paciente, fid_medico, fenfCro, falergias, fantFam, fcreated_by))
        mysql.connection.commit()
        return redirect(url_for('expedientePaciente', id=fid_paciente))


@app.route('/editarExpediente/<id>')
@login_required
@roles_required(['Administrador', 'Medico'])
def editarExpediente(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT Paciente.*, Expediente.* FROM Paciente JOIN Expediente ON Paciente.id = Expediente.id_Paciente WHERE Paciente.id = %s', [id])
    paciente = cur.fetchall()
    return render_template('editarExpediente.html', paciente=paciente)

@app.route('/actualizarExpediente/<id>', methods=['POST'])
@login_required
@roles_required(['Administrador', 'Medico'])
def actualizarExpediente(id):
    if request.method == 'POST' and all(key in request.form for key in ['id_medico', 'id_paciente', 'enfCro', 'alergias', 'antFam', 'created_by']):
        fid_paciente = request.form['id_paciente']
        fid_medico = request.form['id_medico']
        fenfCro = request.form['enfCro']
        falergias = request.form['alergias']
        fantFam = request.form['antFam']
        fcreated_by = request.form['created_by']

        print(f"Datos recibidos: {fid_paciente}, {fid_medico}, {fenfCro}, {falergias}, {fantFam}, {fcreated_by}")

        cur = mysql.connection.cursor()
        cur.execute("UPDATE Expediente SET id_Medico = %s, EnfermedadC = %s, Alergias = %s, AntecedentesFam = %s, created_by = %s WHERE id_Paciente = %s", 
                    (fid_medico, fenfCro, falergias, fantFam, fcreated_by, fid_paciente))
        mysql.connection.commit()
        flash('Expediente actualizado correctamente')
        return redirect(url_for('expedientePaciente', id=fid_paciente))
    else:
        flash('Datos insuficientes para actualizar el expediente')
        return redirect(url_for('expedientePaciente', id=id))

    
@app.route('/buscarExpediente')
@login_required
@roles_required(['Administrador', 'Medico'])
def buscarexpediente():
    return render_template('buscarexpediente.html')

@app.route('/citaPaciente')
def citaPaciente():
    return render_template('citaPaciente.html')

@app.route('/altaPaciente')
def agregarPaciente():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Sexo')
    sexo = cur.fetchall()

    usuario=None
    if session['id_rol'] == 1:
        cur.execute('SELECT * FROM Usuario WHERE id_Rol = 2')
        usuario = cur.fetchall()

    return render_template('agregarPaciente.html', sexo=sexo, usuario=usuario)

@app.route('/guardarPaciente', methods=["POST"])
def guardarPaciente():
    if request.method == 'POST' and 'txtNombre' in request.form and 'txtApePaterno' in request.form and 'txtApeMaterno' in request.form and 'txtFecha' in request.form and 'txtSexo' in request.form and 'txtMedico' in request.form:
        fnombre = request.form['txtNombre']
        fapePaterno = request.form['txtApePaterno']
        fapeMaterno = request.form['txtApeMaterno']
        ffecha = request.form['txtFecha']
        fsexo = request.form['txtSexo']

        if session['id_rol'] == 1:
            fmedico = request.form['txtMedico']
        else:
            fmedico = current_user.id

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Paciente (Nombre, ApePaterno, ApeMaterno, FechaNam, id_Sexo, id_Medico) VALUES (%s, %s, %s, %s, %s,%s)', (fnombre, fapePaterno, fapeMaterno, ffecha, fsexo, fmedico))
        mysql.connection.commit()
        flash('Paciente agregado correctamente', 'success')
        return redirect(url_for('menuPaciente'))
    else:
        flash('Error al agregar paciente', 'error')
        return redirect(url_for('home'))
    
@app.route('/editarPaciente/<id>')
def editarPaciente(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Paciente WHERE id= %s', [id])
    paciente = cur.fetchall()
    cur.execute('SELECT * FROM Sexo')
    sexo = cur.fetchall()
    return render_template('editarPaciente.html', paciente=paciente, sexo=sexo)

@app.route('/actualizarPaciente/<id>', methods=['POST'])
def actualizarPaciente(id):
    if request.method == 'POST':
        nombre = request.form['txtNombre']
        apellidoPa = request.form['txtApePaterno']
        apellidoMa = request.form['txtApeMaterno']
        fecha = request.form['txtFecha']
        sexo = request.form['txtSexo']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Paciente SET Nombre = %s, ApePaterno = %s, ApeMaterno = %s, FechaNam = %s, id_Sexo = %s WHERE id = %s", (nombre, apellidoPa, apellidoMa, fecha, sexo, id))
        mysql.connection.commit()
        flash('Paciente actualizado correctamente')
        return redirect(url_for('menuPaciente'))

@app.route('/eliminarPaciente/<id>')
def eliminarPaciente(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Paciente WHERE id = %s', [id])
    mysql.connection.commit()
    flash('Paciente eliminado correctamente')
    return redirect(url_for('menuPaciente'))

# Ejemplo de vista
@app.route('/ejemplo')
def ejemplo():
    return render_template('ejemplo.html')

@app.route('/cita')
def agregarCita():
    return render_template('citaPaciente.html')

@app.errorhandler(404)
def paginano(e):
    return 'Revisa tu sintaxis: No encontré nada', 404

if __name__ == '__main__':
    csrf.init_app(app)
    app.run(port=3000, debug=True, threaded=True)
