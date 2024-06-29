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

@app.route('/admin')
def admin():
    return render_template('admin.html')

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
            session['id'] = account[0]  # Usa el índice adecuado según tu base de datos
            return redirect(url_for('admin'))
        else:
            flash("RFC o contraseña incorrecta, revisa tus datos", "danger")
            return redirect(url_for('home'))


@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/menuAdmin')
def menuAdm():
    return render_template('menuadmin.html')

@app.errorhandler(404)
def paginano(e):
    return 'Revisa tu sintaxis: No encontré nada', 404

if __name__ == '__main__':
    app.run(port=3000, debug=True, threaded=True)
