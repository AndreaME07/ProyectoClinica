from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_mysqldb import MySQL
from create_database import create_database
from functools import wraps


app = Flask(__name__, template_folder='template')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_clinicamayo'
app.config['MYSQL_UNIX_SOCKET'] = '/opt/lampp/var/mysql/mysql.sock'  
app.secret_key = 'mysecretkey'

mysql = MySQL(app)

create_database()

@app.route('/')
def home():
    return render_template('index.html')

# Función de login
@app.route('/accesoLogin', methods=["GET", "POST"])
def accesoLogin():
    if request.method == 'POST' and 'txtrfc' in request.form and 'txtpassword' in request.form:
        frfc = request.form['txtrfc']
        fpassword = request.form['txtpassword']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Usuario WHERE RFC = %s AND Contrasena = %s', (frfc, fpassword))
        account = cur.fetchone()

        if account:
            session['logueado'] = True
            session['id'] = account[0]  # Usar indice adecuado de acuerdo a la base de datos en este caso db_clinicamayo
            session['id_rol'] = account[8]

            if session['id_rol'] == 1:

                return redirect(url_for('menu'))
            elif session['id_rol'] == 2:
                return redirect(url_for('menuPaciente'))  
        else:
            flash("RFC o contraseña incorrecta, revisa tus datos", "danger")
    return render_template('index.html')

#Decorardor de login
def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if 'logueado' not in session:
            flash('Acceso denegado, inicia sesión para acceder a esta página', 'danger')
            return redirect(url_for('accesoLogin'))
        return f(*args,**kwargs)
    return decorated_function

#Decorador roles
def rol_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session['id_rol'] not in roles:
                flash('No tienes permisos para acceder a esta página', 'danger')
                return redirect(url_for('accesoLogin'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route('/menu')
@login_required
@rol_required(1)
def menu():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Usuario')
    usuario = cur.fetchall()
    return render_template('admin_menu.html', usuario = usuario)

#Funciones de crud Medico
@app.route('/editarMedico/<id>')
@login_required
@rol_required(1)
def editarMedico(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Usuario where id= %s',[id])
    usuario = cur.fetchall()
    cur.execute('SELECT * FROM Rol')
    roles = cur.fetchall()
    return render_template('editarMedico.html', usuario = usuario, roles = roles)

@app.route('/actualizarMedico/<id>', methods = ['POST'])
@login_required
@rol_required(1)
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
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Usuario SET Nombre = %s, ApePaterno = %s, ApeMaterno = %s, RFC = %s, CedulaProfesional = %s, Correo = %s, Contrasena = %s, id_Rol = %s WHERE id = %s", (nombre, apellidoPa, apellidoMa, rfc, cedula, correo, contrasena, rol, id))
        mysql.connection.commit()
        flash('Usuario actualizado correctamente')
        return redirect(url_for('menu'))


@app.route('/buscarMedico')
def buscarMedico():
    return render_template('buscarMedico.html')

@app.route('/eliminarMedico/<id>')
@login_required
@rol_required(1)
def eliminarMedico(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Usuario WHERE id = %s', [id])
    mysql.connection.commit()
    flash('Usuario eliminado correctamente')
    return redirect(url_for('menu'))


@app.route('/altaMedico')
@login_required
@rol_required(1)
def agregarMedico():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Rol')
    roles = cur.fetchall()
    return render_template('agregarMedico.html',roles = roles)

@app.route('/guardarMedico', methods=["POST"])
@login_required
@rol_required(1)
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

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Usuario (Nombre, ApePaterno, ApeMaterno, RFC, CedulaProfesional, Correo, Contrasena, id_Rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (fnombre, fapepaterno, fapematerno, frfc, fcedula, fcorreo, fcontrasena, frol))
        mysql.connection.commit()
        cursor.close()
        
        flash('Médico agregado correctamente', 'success')
        return redirect(url_for('menu'))
    else:
        flash('Error al agregar médico', 'error')
        return redirect(url_for('home'))
##############################################################################################
#Funciones de crud Paciente
@app.route('/menuPaciente')
@login_required
@rol_required(1,2)
def menuPaciente():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Paciente')
    paciente = cur.fetchall()
    return render_template('admin_user.html', paciente = paciente)

@app.route('/diagnosticopaciente')
def diagnosticoPaciente():
    return render_template('diagnosticoPaciente.html')

@app.route('/citaexploracion')
def citaExploracion():
    return render_template('citaExploracion.html')

@app.route('/expedientePaciente')
def expedientePaciente():
    return render_template('expedientePaciente.html')

@app.route('/citaPaciente')
def citaPaciente():
    return render_template('citaPaciente.html')


@app.route('/altaPaciente')
@login_required
@rol_required(1,2)
def agregarPaciente():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Sexo')
    sexo = cur.fetchall()

    return render_template('agregarPaciente.html', sexo = sexo)

@app.route('/guardarPaciente', methods=["POST"])
@login_required
@rol_required(1,2)
def guardarPaciente():
    if request.method == 'POST' and 'txtNombre' in request.form and 'txtApePaterno' in request.form and 'txtApeMaterno' in request.form and 'txtFecha' in request.form and 'txtSexo' in request.form:
        fnombre = request.form['txtNombre']
        fapePaterno = request.form['txtApePaterno']
        fapeMaterno = request.form['txtApeMaterno']
        ffecha = request.form['txtFecha']
        fsexo = request.form['txtSexo']

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Paciente (Nombre, ApePaterno, ApeMaterno, FechaNam, id_Sexo) VALUES (%s, %s, %s, %s, %s)', (fnombre, fapePaterno, fapeMaterno, ffecha, fsexo))
        mysql.connection.commit()
        flash('Paciente agregado correctamente', 'success')
        return redirect(url_for('menuPaciente'))
    else:
        flash('Error al agregar paciente', 'error')
        return redirect(url_for('home'))
    
@app.route('/editarPaciente/<id>')
@login_required
@rol_required(1,2)
def editarPaciente(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Paciente where id= %s',[id])
    paciente = cur.fetchall()
    cur.execute('SELECT * FROM Sexo')
    sexo = cur.fetchall()
    return render_template('editarPaciente.html', paciente = paciente, sexo = sexo)

@app.route('/actualizarPaciente/<id>', methods = ['POST'])
@login_required
@rol_required(1,2)
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
@login_required
@rol_required(1,2)
def eliminarPaciente(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Paciente WHERE id = %s', [id])
    mysql.connection.commit()
    flash('Paciente eliminado correctamente')
    return redirect(url_for('menuPaciente'))


#ejemplo de vista
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
    app.run(port=3000, debug=True, threaded=True)
