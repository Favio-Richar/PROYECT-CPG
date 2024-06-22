# Importación de módulos necesarios para interactuar con la base de datos SQLite
import sqlite3
# Importación del módulo para manejar operaciones de archivo CSV
import csv
# Importación de funciones de fecha y tiempo para manejar y calcular fechas
from datetime import datetime, timedelta
# Importación de getpass para ocultar la entrada de contraseñas en la consola
import getpass
# Importación del módulo random para generar números aleatorios
import random

# Función para registrar un nuevo usuario
def registrar_usuario(cursor):
    while True:
        username = input("Ingrese el nombre de usuario: ")
        # Verificar si el nombre de usuario ya existe en la base de datos
        cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        if cursor.fetchone():
            print("El nombre de usuario ya existe. Intente con otro.")
        else:
            break
    password = getpass.getpass("Ingrese la contraseña: ")
    # Insertar el nuevo usuario en la base de datos
    cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
    print("Usuario registrado correctamente.")

# Función para autenticar un usuario
def login(cursor):
    username = input("Ingrese su nombre de usuario: ")
    password = getpass.getpass("Ingrese su contraseña: ")
    # Verificar si las credenciales son correctas
    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
    if cursor.fetchone():
        print("Inicio de sesión exitoso.")
        return True
    else:
        print("Nombre de usuario o contraseña incorrectos.")
        return False

# Función para insertar una nueva venta en la base de datos
def insertar_venta(cursor):
    fecha = datetime.now().strftime('%Y-%m-%d')
    producto = input("Ingrese el nombre del producto: ")
    categoria = input("Ingrese la categoría del producto: ")
    
    # Validación y captura del precio
    while True:
        try:
            precio = float(input("Ingrese el precio del producto: "))
            if precio < 0:
                raise ValueError("El precio no puede ser negativo.")
            break
        except ValueError as e:
            print("Entrada inválida. Por favor ingrese un número válido para el precio. Error:", e)
    
    # Validación y captura de la cantidad
    while True:
        try:
            cantidad = int(input("Ingrese la cantidad vendida: "))
            if cantidad < 0:
                raise ValueError("La cantidad no puede ser negativa.")
            break
        except ValueError as e:
            print("Entrada inválida. Por favor ingrese un número entero válido para la cantidad. Error:", e)
    
    total = precio * cantidad

    # Insertar la venta en la base de datos
    cursor.execute('''INSERT INTO ventas (fecha, producto, categoria, precio, cantidad, total)
                    VALUES (?, ?, ?, ?, ?, ?)''', (fecha, producto, categoria, precio, cantidad, total))

    print("Venta insertada correctamente.")

# Función para agregar ventas aleatorias
def agregar_ventas_aleatorias(cursor, num_ventas):
    fecha_base = datetime.now()
    productos = [
        # Lista de productos para generar datos aleatorios
        ("Televisor LED 42\"", "Electrónica", 299000),
        ("Smartphone 128GB", "Electrónica", 599000),
        ("Laptop 15\"", "Electrónica", 799000),
        ("Licuadora", "Hogar y Cocina", 49000),
        ("Olla de Presión", "Hogar y Cocina", 29000),
        ("Juego de Sartenes", "Hogar y Cocina", 79000),
        ("Camiseta", "Ropa y Accesorios", 19000),
        ("Pantalones Jeans", "Ropa y Accesorios", 39000),
        ("Gafas de Sol", "Ropa y Accesorios", 49000),
        ("Bicicleta de Montaña", "Deportes y Aire Libre", 299000),
        ("Pelota de Fútbol", "Deportes y Aire Libre", 24000),
        ("Raqueta de Tenis", "Deportes y Aire Libre", 79000),
        ("Libro de Ficción", "Libros y Papelería", 14000),
        ("Cuaderno de Notas", "Libros y Papelería", 4000),
        ("Pluma Estilográfica", "Libros y Papelería", 29000)
    ]

    # Insertar ventas aleatorias en la base de datos
    for _ in range(num_ventas):
        fecha = fecha_base - timedelta(days=random.randint(0, 11))
        producto, categoria, precio = random.choice(productos)
        cantidad = random.randint(1, 10)
        total = precio * cantidad
        cursor.execute('''INSERT INTO ventas (fecha, producto, categoria, precio, cantidad, total)
                        VALUES (?, ?, ?, ?, ?, ?)''', (fecha.strftime('%Y-%m-%d'), producto, categoria, precio, cantidad, total))

    print(f"{num_ventas} ventas aleatorias insertadas correctamente.")

# Función para exportar datos a un archivo CSV
def exportar_csv(cursor):
    # Consultar y escribir los datos de ventas en un archivo CSV
    cursor.execute("SELECT * FROM ventas")
    with open('ventas.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([i[0] for i in cursor.description])  # Escribir encabezados
        csv_writer.writerows(cursor.fetchall())

    print("Datos exportados a ventas.csv correctamente.")

# Crear una conexión a la base de datos SQLite
conn = sqlite3.connect('ventas.db')
cursor = conn.cursor()

# Crear la tabla usuarios si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )''')

# Crear la tabla ventas si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT,
                    producto TEXT,
                    categoria TEXT,
                    precio REAL,
                    cantidad INTEGER,
                    total REAL
                )''')

# Menú de registro y login
while True:
    print("\n1. Registrar usuario")
    print("2. Iniciar sesión")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == '1':
        registrar_usuario(cursor)
        conn.commit()
    elif opcion == '2':
        if login(cursor):
            break
    elif opcion == '3':
        conn.close()
        exit()
    else:
        print("Opción no válida. Intente de nuevo.")

# Menú principal después del login
while True:
    print("\n1. Insertar venta")
    print("2. Agregar ventas aleatorias")
    print("3. Exportar a CSV")
    print("4. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == '1':
        insertar_venta(cursor)
        conn.commit()
    elif opcion == '2':
        num_ventas = int(input("Ingrese el número de ventas aleatorias a agregar: "))
        agregar_ventas_aleatorias(cursor, num_ventas)
        conn.commit()
    elif opcion == '3':
        exportar_csv(cursor)
    elif opcion == '4':
        break
    else:
        print("Opción no válida. Intente de nuevo.")

# Cerrar la conexión a la base de datos
conn.close()

print("Programa finalizado.")
