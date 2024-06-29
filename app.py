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

@app.errorhandler(404)
def paginano(e):
    return 'Revisa tu sintaxis: No encontré nada', 404

if __name__ == '__main__':
    app.run(port=3000, debug=True, threaded=True)
