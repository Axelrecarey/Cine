import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('Peliculas.db')
cursor = conn.cursor()

# Verificar las tablas disponibles
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()
print("Tablas en la base de datos:", tablas)


if ('PELICULAS',) in tablas:
    # Obtener la estructura de la tabla
    cursor.execute("PRAGMA table_info(PELICULAS)")
    columnas = cursor.fetchall()
    nombres_columnas = [col[1] for col in columnas]
    
    # Añadir columna Fecha_estreno si no existe
    if 'Fecha_estreno' not in nombres_columnas:
        cursor.execute("ALTER TABLE PELICULAS ADD COLUMN Fecha_estreno TEXT")
        conn.commit()
        print("Columna 'Fecha_estreno' añadida a la tabla PELICULAS.")
    
    # Ejecutar una consulta para seleccionar todos los registros de la tabla PELICULAS
    cursor.execute("SELECT * FROM PELICULAS")
    peliculas = cursor.fetchall()
    
    if peliculas:
        print("Datos de la tabla PELICULAS:")
        for pelicula in peliculas:
            print(pelicula)
        
        # Actualizar las fechas de estreno para las películas existentes
        fechas_estreno = {
            'El Último Viaje': '2026-03-15',
            'Sombras del Pasado': '2026-05-20',
            'Risas Inesperadas': '2026-07-10',
            'Guerra de Titanes': '2026-09-05',
            'Misterio en la Niebla': '2026-11-12',
            'Amor Eterno': '2026-02-28',
            'Exploradores del Abismo': '2026-04-18',
            'La Rebelión': '2026-06-22',
            'Código Secreto': '2026-08-30',
            'Sueños Perdidos': '2026-10-14'
        }
        
        for nombre, fecha in fechas_estreno.items():
            cursor.execute("UPDATE PELICULAS SET Fecha_estreno = ? WHERE Nombre = ?", (fecha, nombre))
        conn.commit()
        print("Fechas de estreno actualizadas.")
        
        # Mostrar los datos actualizados
        cursor.execute("SELECT * FROM PELICULAS")
        peliculas_actualizadas = cursor.fetchall()
        print("Datos actualizados de la tabla PELICULAS:")
        for pelicula in peliculas_actualizadas:
            print(pelicula)
    else:
        print("La tabla PELICULAS está vacía.")
        
        # 10 películas de 2026 con fecha de estreno
        peliculas_a_insertar = [
            ('El Último Viaje', 1, 'Ciencia Ficción', 12, 120, 'Una aventura épica en el espacio.', 8.5, '2026-03-15'),
            ('Sombras del Pasado', 2, 'Drama', 15, 95, 'Una historia de redención y amor.', 7.8, '2026-05-20'),
            ('Risas Inesperadas', 3, 'Comedia', 7, 85, 'Una comedia ligera sobre malentendidos.', 6.9, '2026-07-10'),
            ('Guerra de Titanes', 1, 'Acción', 18, 140, 'Batallas épicas entre dioses y humanos.', 9.0, '2026-09-05'),
            ('Misterio en la Niebla', 4, 'Thriller', 16, 110, 'Un detective resuelve un crimen en una ciudad brumosa.', 8.2, '2026-11-12'),
            ('Amor Eterno', 2, 'Romance', 12, 100, 'Una historia de amor que trasciende el tiempo.', 7.5, '2026-02-28'),
            ('Exploradores del Abismo', 1, 'Aventura', 10, 125, 'Una expedición al fondo del océano.', 8.7, '2026-04-18'),
            ('La Rebelión', 3, 'Fantasía', 14, 130, 'Una joven lucha contra un régimen opresivo.', 8.0, '2026-06-22'),
            ('Código Secreto', 4, 'Suspenso', 17, 105, 'Espías en una misión de alto riesgo.', 7.9, '2026-08-30'),
            ('Sueños Perdidos', 2, 'Drama', 13, 90, 'Reflexiones sobre la vida y las decisiones.', 8.1, '2026-10-14')
        ]
        
        cursor.executemany("INSERT INTO PELICULAS (Nombre, Proveedor, Generos, Clasificacion, Duracion, Descripcion, Calificacion, Fecha_estreno) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", peliculas_a_insertar)
        conn.commit()
        print("Se han insertado 10 películas en la tabla PELICULAS con fechas de estreno.")
        
        # Mostrar los datos después de la inserción
        cursor.execute("SELECT * FROM PELICULAS")
        peliculas = cursor.fetchall()
        print("Datos de la tabla PELICULAS:")
        for pelicula in peliculas:
            print(pelicula)
else:
    print("La tabla PELICULAS no existe en la base de datos.")

# Cerrar la conexión
conn.close()
