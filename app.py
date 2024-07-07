from flask import Flask, render_template, redirect, request, session, flash, url_for
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

# Función de login
@app.route('/accesoLogin', methods=["GET", "POST"])
def accesoLogin():
    if request.method == 'POST' and 'txtrfc' in request.form and 'txtpassword' in request.form:
        frfc = request.form['txtrfc']
        fpassword = request.form['txtpassword']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM t_login WHERE rfc = %s AND password = %s', (frfc, fpassword))
        account = cur.fetchone()

        if account:
            session['logueado'] = True
            session['id'] = account[0]  # Usar indice adecuado de acuerdo a la base de datos en este caso db_clinicamayo
            session['id_rol'] = account[3]

            if session['id_rol'] == 1:
                return render_template("admin_menu.html")
            elif session['id_rol'] == 2:
                return render_template("expedientePaciente.html")  
        else:
            flash("RFC o contraseña incorrecta, revisa tus datos", "danger")
            return redirect(url_for('home'))


@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/admin_menu')
def admin_menu():
    return render_template('admin_menu.html')

@app.route('/agregarMedico')
def agregarMedico():
    return render_template('agregarMedico.html')

@app.route('/editarMedico')
def editarMedico():
    return render_template('editarMedico.html')

@app.route('/buscarMedico')
def buscarMedico():
    return render_template('buscarMedico.html')


@app.route('/diagnosticopaciente')
def diagnosticoPaciente():
    return render_template('diagnosticoPaciente.html')

@app.route('/citaexploracion')
def citaExploracion():
    return render_template('citaExploracion.html')

@app.route('/expedientePaciente')
def expedientePaciente():
    return render_template('expedientePaciente.html')

@app.route('/editarPaciente')
def editarPaciente():
    return render_template('editarPaciente.html')

@app.route('/citaPaciente')
def citaPaciente():
    return render_template('citaPaciente.html')

@app.route('/agregarPaciente')
def agregarPaciente():
    return render_template('agregarPaciente.html')



#ejemplo de vista
@app.route('/ejemplo')
def ejemplo():
    return render_template('ejemplo.html')
    
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
