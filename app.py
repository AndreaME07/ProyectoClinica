from flask import Flask, render_template, redirect, request, session, flash, url_for,logging
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='template')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_clinicamayo'
app.secret_key = 'mysecretkey'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    if 'logueado' in session:
        return render_template('admin.html')
    else:
        flash('Por favor, inicie sesión primero.', 'error')
        return redirect(url_for('home'))

@app.route('/accesoLogin', methods=["GET", "POST"])
def Login():
    if request.method == 'POST' and 'txtRFC' in request.form and 'txtPassword' in request.form:
        frfc = request.form['txtRFC']
        fpassword = request.form['txtPassword']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM t_login WHERE RFC = %s AND Password = %s', (frfc, fpassword))
        account = cursor.fetchone()

        if account:
            session['logueado'] = True
            session['id'] = account['id']
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
            return redirect(url_for('home'))
    else:
        flash('Por favor ingrese sus credenciales', 'error')
        return redirect(url_for('home'))
    
@app.route('/altaMedico')
def agregarMedico():
    return render_template('agregarMedico.html')

@app.route('/guardarMedico', methods=["POST"])
def guardarMedico():
    if request.method == 'POST' and 'txtNombre' in request.form and 'txtApellido' in request.form and 'txtEspecialidad' in request.form:
        fnombre = request.form['txtNombre']
        fapellido = request.form['txtApellido']
        fespecialidad = request.form['txtEspecialidad']

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO t_medico (Nombre, Apellido, Especialidad) VALUES (%s, %s, %s)', (fnombre, fapellido, fespecialidad))
        mysql.connection.commit()
        flash('Médico agregado correctamente', 'success')
        return redirect(url_for('admin'))
    else:
        flash('Error al agregar médico', 'error')
        return redirect(url_for('home'))
    

@app.route('/altaPaciente')
def agregarPaciente():
    return render_template('agregarPaciente.html')

@app.route('/guardarPaciente', methods=["POST"])
def guardarPaciente():
    if request.method == 'POST' and 'txtNombre' in request.form and 'txtApellido' in request.form and 'txtEdad' in request.form and 'txtSexo' in request.form:
        fnombre = request.form['txtNombre']
        fapellido = request.form['txtApellido']
        fedad = request.form['txtEdad']
        fsexo = request.form['txtSexo']

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO t_paciente (Nombre, Apellido, Edad, Sexo) VALUES (%s, %s, %s, %s)', (fnombre, fapellido, fedad, fsexo))
        mysql.connection.commit()
        flash('Paciente agregado correctamente', 'success')
        return redirect(url_for('admin'))
    else:
        flash('Error al agregar paciente', 'error')
        return redirect(url_for('home'))

    
@app.route('/Cita')
def agregarCita():
    return render_template('citaPaciente.html')

@app.route('/expedienteP')
def expedientePaciente():
    return render_template('expedientePaciente.html')

@app.route('/altaPaceinte')
def agregarPaciente():
    return render_template('agregarPaciente.html')

@app.route('/editarPaciente')
def editarPaciente():
    return render_template('editarPaciente.html')
    
@app.route('/altaMedico')
def agregarMedico():
    return render_template('agregarMedico.html')
    
@app.route('/editarMedico')
def editarMedico():
    return render_template('editarMedico.html')


@app.errorhandler(404)
def paginano(e):
    return 'Revisa tu sintaxis: No encontré nada', 404

if __name__ == '__main__':
    app.run(port=3000, debug=True, threaded=True)
