from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Mysql conecxion
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'administracioninmo'
mysql = MySQL(app)

# configuracion
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes')
    data = cur.fetchall()
    return render_template('index.html', clientes = data)

@app.route('/add_contact', methods=['POST'])   
def add_contact():
    if request.method == 'POST':
       nombre = request.form['nombre']
       apellido = request.form['apellido']
       direccion = request.form['direccion']
       localidad = request.form['localidad']
       telefono = request.form['telefono']
       email = request.form['email']
       cur = mysql.connection.cursor()
       cur.execute('INSERT INTO clientes (nombre, apellido, direccion, localidad, telefono, email) VALUES (%s, %s, %s, %s, %s, %s)',
       (nombre, apellido, direccion, localidad, telefono, email)) 
       mysql.connection.commit()
       flash('El cliente se agrego correctamente') 
       return redirect(url_for('Index'))

#Editar
@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])   
def update_contact(id):
    if request.method == 'POST':
     nombre = request.form['nombre']
     apellido = request.form['apellido']
     direccion = request.form['direccion']
     localidad = request.form['localidad']
     telefono = request.form['telefono']
     email = request.form['email']
     cur = mysql.connection.cursor()
     cur.execute("""
        UPDATE clientes
        SET nombre = %s,
            apellido = %s,
            direccion = %s,
            localidad = %s,
            telefono = %s,
            email = %s
        WHERE id = %s   
    """, (nombre, apellido, direccion, localidad, telefono, email, id))
    mysql.connection.commit()
    flash('El contacto se edito correctamente')
    return redirect(url_for('Index'))

#Eliminar 

@app.route('/delete/<string:id>')    
def delete_contact(id):
   cur = mysql.connection.cursor() 
   cur.execute('DELETE FROM clientes WHERE id = {0}' .format(id))
   mysql.connection.commit()
   flash('Contacto removido')
   return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port = 3000, debug = True)