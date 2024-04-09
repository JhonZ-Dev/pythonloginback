from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'pproyect'
mysql = MySQL(app)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['nombre']
    password = data['contrasenia']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE nombre = %s", (username,))
    user = cur.fetchone()
    cur.close()
    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({'message': 'Login exitoso!'})
        else:
            return jsonify({'message': 'Credenciales incorrectas'}), 401
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['nombre']
    lastname = data['apellido']
    password = data['contrasenia']
    age = data['edad']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE nombre = %s", (username,))
    user = cur.fetchone()
    if user:
        cur.close()
        return jsonify({'message': 'El usuario ya existe'}), 409  # 409 Conflict
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cur.execute("INSERT INTO users (nombre, apellido,contrasenia,edad) VALUES (%s, %s,%s,%s)", (username,lastname, hashed_password, age))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201  # 201 Created
if __name__ == '__main__':
    app.run(debug=True)