from flask import Blueprint, jsonify, request
from database import mysql
from script import jsonFormatArray, jsonFormat

fnb = Blueprint('fnb', __name__)

@fnb.route('/fnb', methods=['GET', 'POST'])
def fnbDefault():
    cursor = mysql.connection.cursor()
    auth_header = request.headers.get("Authorization")

    valid = checkToken(auth_header, cursor)
    
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
            "nama": json_data['name'],
            "alamat": json_data['alamat'],
            "titik_koordinat": json_data['titik_koordinat'],
        }
        cursor.execute(' INSERT INTO fnb(alamat, nama, titik_koordinat) VALUES (%s, %s, %s) ', (data["alamat"], data["nama"], data["titik_koordinat"]))

        return jsonify(data), 201

@fnb.route('/fnb/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def fnById(id):
    cursor = mysql.connection.cursor()

    if (request.method == 'GET'):
        cursor.execute(' SELECT * FROM fnb WHERE id=%s ', (id,)) 

        res = jsonFormat(cursor)

        cursor.close()
        return jsonify(res), 200

    elif (request.method == 'PUT'):     
        json_data = request.json
        data = {
            "nama": json_data['name'],
            "alamat": json_data['alamat'],
            "titik_koordinat": json_data['titik_koordinat'],
        }
        
        cursor.execute(' UPDATE fnb SET alamat=%s, nama=%s, titik_koordinat=%s WHERE id=%s', (data["alamat"], data["nama"], data["titik_koordinat"], id))

        return jsonify(data), 201

    elif (request.method == 'DELETE'):
        cursor.execute(' DELETE FROM fnb WHERE id=%s ', (id))

        return "Deleted", 202


def checkToken(token, cursor):
    cursor.execute(' SELECT * FROM session WHERE token=%s ', (token,))

    res = jsonFormat(cursor)

    return res
