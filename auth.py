from flask import Blueprint, jsonify, request, make_response
from database import mysql
import jwt
from script import verifyUser, jsonFormat, encodeStr

auth = Blueprint('auth', __name__)

@auth.route('/log-in', methods=['POST'])
def logIn():
  cursor = mysql.connection.cursor()
  json_data = request.json

  data = {
    "name": json_data['name'],
    "password": json_data['password'],
  }
  print(data, 'line 17')

  cursor.execute(' SELECT * FROM user WHERE name=%s ', ("thoriqzs",))
  resUser = jsonFormat(cursor)

  info = checkSessionAvailable(cursor, resUser)
  if (info):
    return jsonify(
      {
        'message': 'We found your session have already started! Happy coding :D', 
        'token' : info['token']
      }), 200

  if (resUser):
    if (verifyUser(data['password'], resUser['password'])):
      token = jwt.encode({'user_id' : resUser['id'] }, 'superdupersecretkey')
      print(token)
      try:
        cursor.execute(' INSERT INTO session(user_id, token) VALUES (%s, %s) ', (resUser['id'], token))
        mysql.connection.commit() 
        cursor.close()
      except:
        return "Unable to make new session! Your session have already started"
      return jsonify(
        {
          'message': 'Please save this token and use it to access our provided API!', 
          'token' : token
        }), 201
    
    else:
      return "Wrong Username or Password", 401

  return "Username Not Found", 404

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
    print(encodedPass)

    cursor.execute(' INSERT INTO user(name, password) VALUES (%s, %s) ', (data['name'], encodedPass))

    mysql.connection.commit()
    cursor.close()
    return "Success Creating New Account!", 201
  # auth = request.authorization
  # if (auth):
  #   token = jwt.encode({'user' : auth.username }, 'superdupersecretkey')
  #   print(jsonify({'token' : token}))

  #   return jsonify({'token' : token})

  # return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

def checkUserAvailable(cursor, data):
  cursor.execute(' SELECT * FROM user WHERE name=%s AND password=%s ', (data['name'], data['password']))
  res = jsonFormat(cursor)

  return res

def checkSessionAvailable(cursor, data):
  print(data, 'line 87')
  cursor.execute(' SELECT * FROM session WHERE user_id=%s ', (data['id'],))
  res = jsonFormat(cursor)

  return res