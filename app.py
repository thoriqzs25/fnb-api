from flask import Flask
from database import mysql
from fnb import fnb
from auth import auth

app = Flask(__name__)
 
app.register_blueprint(auth)
app.register_blueprint(fnb)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tubes_tst'
app.config['MYSQL_UNIX_SOCKET'] = '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
app.config["FLASK_DEBUG"] = 1

mysql.init_app(app)

@app.route('/', methods=['GET'])
def default():
    return "Hello User"

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=105)
    app.run(debug=True)

# mysql.connection.commit()