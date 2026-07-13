import sqlite3
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

DB_NAME = 'usuarios.db'

# 1. Crear Base de Datos y Tabla de Usuarios
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 2. Función auxiliar para encriptar claves usando SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 3. Insertar integrantes en la base de datos (poblar datos de prueba)
def poblar_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Nombres de tus integrantes y sus claves (cambia o agrega según corresponda)
    integrantes = [
        ("Guillermo Carrasco", hash_password("secreta123")),
        ("Nombre2 Apellido2", hash_password("claveSegura456")),
        ("Nombre3 Apellido3", hash_password("accesoPrueba789"))
    ]
    
    for nombre, clave_hash in integrantes:
        try:
            cursor.execute("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", (nombre, clave_hash))
        except sqlite3.IntegrityError:
            # Si el usuario ya existe por una ejecución previa, simplemente lo omite
            pass
            
    conn.commit()
    conn.close()

# 4. Ruta del Servidor API Web para Validación
@app.route('/validar', methods=['POST'])
def validar_usuario():
    # Obtener el payload enviado en formato JSON
    data = request.json
    if not data:
        return jsonify({"mensaje": "Error: No se enviaron datos en formato JSON."}), 400
        
    usuario = data.get('nombre')
    password = data.get('password')
    
    if not usuario or not password:
        return jsonify({"mensaje": "Error: Campos 'nombre' y 'password' son requeridos."}), 400
    
    # Encriptar la contraseña recibida para compararla con la guardada
    hash_ingresado = hash_password(password)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nombre=? AND password_hash=?", (usuario, hash_ingresado))
    user = cursor.fetchone()
    conn.close()
    
    # Respuesta condicional de la autenticación
    if user:
        return jsonify({
            "mensaje": f"Autenticación exitosa. Bienvenido {usuario}.",
            "estado": "Conectado"
        }), 200
    else:
        return jsonify({
            "mensaje": "Error de autenticación: Credenciales inválidas."
        }), 401

if __name__ == '__main__':
    init_db()
    poblar_db()
    print("Base de datos creada y poblada exitosamente.")
    print("Iniciando servidor web Flask en http://127.0.0.1:7500 ...")
    app.run(port=7500, debug=False)
