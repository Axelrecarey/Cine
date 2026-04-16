from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from Validacion_admin import validar_administrador, administradores

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambiar esto por una clave un poco mas segura

def get_db_connection():
    conn = sqlite3.connect('Peliculas.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ingreso como admin

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario'].strip()
        contraseña = request.form['contraseña'].strip()
        if usuario in administradores and contraseña == administradores[usuario]['password']:
            session['usuario'] = administradores[usuario]['nombre']
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error='Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/admin')
def admin():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    peliculas = conn.execute('SELECT rowid, * FROM PELICULAS').fetchall()
    conn.close()
    return render_template('admin_peliculas.html', peliculas=peliculas, usuario=session['usuario'])

# Agregar Pelicula
@app.route('/add_pelicula', methods=['POST'])
def add_pelicula():
    nombre = request.form['nombre']
    proveedor = int(request.form['proveedor'])
    generos = request.form['generos']
    clasificacion = int(request.form['clasificacion'])
    duracion = int(request.form['duracion'])
    descripcion = request.form['descripcion']
    calificacion = float(request.form['calificacion'])
    fecha_estreno = request.form['fecha_estreno']
    conn = get_db_connection()
    conn.execute('INSERT INTO PELICULAS (Nombre, Proveedor, Generos, Clasificacion, Duracion, Descripcion, Calificacion, Fecha_estreno) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                 (nombre, proveedor, generos, clasificacion, duracion, descripcion, calificacion, fecha_estreno))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

# Editar pelicula
@app.route('/edit_pelicula', methods=['POST'])
def edit_pelicula():
    id = int(request.form['id'])
    nombre = request.form['nombre']
    proveedor = int(request.form['proveedor'])
    generos = request.form['generos']
    clasificacion = int(request.form['clasificacion'])
    duracion = int(request.form['duracion'])
    descripcion = request.form['descripcion']
    calificacion = float(request.form['calificacion'])
    fecha_estreno = request.form['fecha_estreno']
    conn = get_db_connection()
    conn.execute('UPDATE PELICULAS SET Nombre=?, Proveedor=?, Generos=?, Clasificacion=?, Duracion=?, Descripcion=?, Calificacion=?, Fecha_estreno=? WHERE rowid=?',
                 (nombre, proveedor, generos, clasificacion, duracion, descripcion, calificacion, fecha_estreno, id))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

# Eliminar pelicula
@app.route('/delete_pelicula', methods=['POST'])
def delete_pelicula():
    id = int(request.form['id'])
    conn = get_db_connection()
    conn.execute('DELETE FROM PELICULAS WHERE rowid=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)