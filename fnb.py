from flask import Blueprint, jsonify, request
from database import mysql
from script import jsonFormatArray, jsonFormat
from script import tokenKey, dateFormat
import jwt
from datetime import datetime

fnb = Blueprint('fnb', __name__)

@fnb.route('/fnb', methods=['GET', 'POST'])
def fnbDefault():
    
    cursor = mysql.connection.cursor()

    auth_header = request.headers.get("Authorization")

    valid = checkToken(auth_header)
    valid = True
    
    if not valid:
        return "Token not valid", 404

    if (request.method == 'GET'):
        cursor.execute(' SELECT * FROM fnb ')

        res = jsonFormatArray(cursor)

        cursor.close()
        return jsonify(res), 200
    
    elif (request.method == 'POST'):
        json_data = request.json
        data = {
            "nama": json_data['nama'],
            "alamat": json_data['alamat'],
            "titik_koordinat": json_data['titik_koordinat'],
        }
        cursor.execute(' INSERT INTO fnb(alamat, nama, titik_koordinat) VALUES (%s, %s, %s) ', (data["alamat"], data["nama"], data["titik_koordinat"]))

        return jsonify(data), 201

@fnb.route('/fnb/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def fnById(id):
    cursor = mysql.connection.cursor()
    auth_header = request.headers.get("Authorization")

    valid = checkToken(auth_header)
    valid = True
    
    if not valid:
        return "Token not valid", 404


    if (request.method == 'GET'):
        cursor.execute(' SELECT * FROM fnb WHERE id=%s ', (id,)) 

        res = jsonFormat(cursor)

        cursor.close()
        return jsonify(res), 200

    elif (request.method == 'PUT'):     
        json_data = request.json
        data = {
            "nama": json_data['nama'],
            "alamat": json_data['alamat'],
            "titik_koordinat": json_data['titik_koordinat'],
        }
        
        cursor.execute(' UPDATE fnb SET alamat=%s, nama=%s, titik_koordinat=%s WHERE id=%s', (data["alamat"], data["nama"], data["titik_koordinat"], id))

        return jsonify(data), 201

    elif (request.method == 'DELETE'):
        cursor.execute(' DELETE FROM fnb WHERE id=%s ', (id,))

        return "Deleted, have a nice day!", 202


def checkToken(bearer):
    try:
        token = bearer.split()[1]
        decodedToken = jwt.decode(token, tokenKey, algorithms=['HS256'])
        date_str = decodedToken['exp_date']
        tokenDate = datetime.strptime(date_str, dateFormat)
        if (tokenDate < datetime.now()):
            raise

        return True
    except:
        return False

@fnb.route('/dev/addkategori', methods=['GET'])
def manipulateDb():
    cursor = mysql.connection.cursor()
    
    cursor.execute('SELECT * FROM fnb')
    fnbData = jsonFormatArray(cursor)

    for fnb in fnbData:
        nama = str(fnb['nama'].lower()) 
        if (('resto' in nama) or ('restaurant' in nama) or 'kitchen' in nama):
            print('RESTO')
            cat = 'Restoran'
        elif (('kafe' in nama) or ('coffee' in nama) or ('cafe' in nama) or 'kopi' in nama):
            cat = 'Cafe'
        elif (('warung' in nama)):
            cat = 'Warung'
        elif (('rm' in nama) or ('rumah' in nama)):
            cat = 'Rumah Makan'
        elif (('bbq' in nama) or ('suki' in nama)):
            cat = 'AYCE'
        else:
            cat = 'DLL'

        print(cat, fnb['id'])
        
        addKategori(cat, fnb['id'])

    return "Sukses!!"

@fnb.route('/dev/createcol', methods=['GET'])
def createCol():
    cursor = mysql.connection.cursor()

    cursor.execute('ALTER TABLE fnb ADD COLUMN kategori VARCHAR(64)')
    mysql.connection.commit()

def addKategori (kategori, id):
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE fnb SET kategori=%s WHERE id=%s', (kategori, id))
    mysql.connection.commit()