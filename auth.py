from flask import Blueprint, jsonify, request, make_response
from database import mysql
import jwt
from script import verifyUser, jsonFormat, encodeStr, tokenKey, dateFormat
from datetime import datetime, timedelta

auth = Blueprint('auth', __name__)

@auth.route('/log-in', methods=['POST'])
def logIn():
  cursor = mysql.connection.cursor()
  json_data = request.json

  data = {
    "name": json_data['name'],
    "password": json_data['password'],
  }

  cursor.execute(' SELECT * FROM user WHERE name=%s ', (data['name'],))
  resUser = jsonFormat(cursor)

  if (resUser):
    if (verifyUser(data['password'], resUser['password'])):
      date = datetime.now() + timedelta(days=7)
      date_str = date.strftime(dateFormat)
      token = jwt.encode({'exp_date' : date_str}, tokenKey)
    
      return jsonify(
        {
          'message': 'Please save this token and use it to access our provided API! This token will last for 7 Days',
          'token' : token
        }), 201
    
    else:
      return "Wrong Username or Password", 401

  return "No available username! Please sign in", 404

@auth.route('/sign-in', methods=['POST'])
def signIn():
  cursor = mysql.connection.cursor()
  json_data = request.json

  data = {
    "name": json_data['name'],
    "password": json_data['password'],
  }

  if checkUserAvailable(cursor, data):
    return "Your Username or Password is already being used!", 401

  else:
    encodedPass = encodeStr(data['password'])

    cursor.execute(' INSERT INTO user(name, password) VALUES (%s, %s) ', (data['name'], encodedPass))

    mysql.connection.commit()
    cursor.close()
    return "Success Creating New Account!", 201

def checkUserAvailable(cursor, data):
  print(data)
  cursor.execute(' SELECT * FROM user WHERE name=%s', (data['name'],))
  res = jsonFormat(cursor)
  print(res)

  return res