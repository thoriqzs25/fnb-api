from flask import Flask, session, jsonify
from script import jsonFormatArray
from database import mysql
from fnb import fnb
from auth import auth
from otp import mail
from geopy.geocoders import Nominatim

app = Flask(__name__)
 
app.register_blueprint(auth)
app.register_blueprint(fnb)

app.config["SECRET_KEY"] = "secret"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tubes_tst'
app.config['MYSQL_UNIX_SOCKET'] = '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
app.config["FLASK_DEBUG"] = 1

app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "imap.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_DEFAULT_SENDER"] = "thariqzsatyagraha@gmail.com"
app.config["MAIL_USERNAME"] = "thariqzsatyagraha@gmail.com"
app.config["MAIL_PASSWORD"] = "tobr yhrm dslg hlbu"

mysql.init_app(app)
mail.init_app(app)

@app.route('/', methods=['GET'])
def default():
    return "Hello User"

@app.route('/loc', methods=['GET'])
def loc():
    geolocator = Nominatim(user_agent="aplikasi-saya")

# Konversi alamat jalan menjadi koordinat geografis
    lokasi = geolocator.geocode("Jl. Pemuda No. 3, Bandung, Jawa Barat")

    # Cetak latitude dan longitude dari alamat tersebut
    print(lokasi.latitude, lokasi.longitude)
    return "latlong"

@app.route('/db', methods=['GET'])
def user():
    cursor = mysql.connection.cursor()
    cursor.execute(' SELECT * FROM user ')

    res = jsonFormatArray(cursor)

    cursor.close()
    return jsonify(res), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
    # app.run(debug=True)

# mysql.connection.commit()