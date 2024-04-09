from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'usuario_mysql'
app.config['MYSQL_PASSWORD'] = 'contraseña_mysql'
app.config['MYSQL_DB'] = 'nombre_basedatos'
mysql = MySQL(app)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            # Aquí puedes devolver algún token JWT si lo deseas
            return jsonify({'message': 'Login exitoso!'})
        else:
            return jsonify({'message': 'Credenciales incorrectas'}), 401
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)