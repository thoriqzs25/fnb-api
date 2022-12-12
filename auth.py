from flask import Blueprint, jsonify, request, make_response, session
from database import mysql
import jwt
from script import verifyUser, jsonFormat, encodeStr, tokenKey, dateFormat, otpHandler
from datetime import datetime, timedelta
import re

auth = Blueprint('auth', __name__)

@auth.route('/log-in', methods=['POST'])
def logIn():
  cursor = mysql.connection.cursor()
  json_data = request.json

  data = {
    "email": json_data['email'],
    "password": json_data['password'],
  }

  cursor.execute(' SELECT * FROM user WHERE email=%s ', (data['email'],))
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
      return "Wrong Email or Password", 401

  return "No available user! Please sign in", 404

@auth.route('/sign-in', methods=['POST'])
def signIn():

  cursor = mysql.connection.cursor()
  json_data = request.json

  otp = request.args.get('otp')
  if (otp):
    return checkOTP(otp)

  data = {
    "email": json_data['email'],
    "password": json_data['password'],
  }
  session['user_cred'] = data

  if not validEmail(data['email']):
    return "Please enter a valid Email", 401

  if checkUserAvailable(cursor, data):
    return "Your Email is already being used!", 401

  else:
    try:
      res = otpHandler(data)
    except:
      return "Failed to send OTP! Please retry!", 400
    return res, 200

def checkOTP(otp):
  sessionOtp = session.get('otp')
  if (otp == sessionOtp):
    try:
      createUser()
    except:
      return "Failed to create user", 400
    
    session.clear()
    return "Success creating new account!", 201

  else: 
    return "Wrong OTP!", 200

def createUser():
  cursor = mysql.connection.cursor()
  data = session.get('user_cred')
  print(data, 'line 89 DATA')

  encodedPass = encodeStr(data['password'])

  cursor.execute(' INSERT INTO user(email, password) VALUES (%s, %s) ', (data['email'], encodedPass))

  mysql.connection.commit()
  cursor.close()

def checkUserAvailable(cursor, data):
  cursor.execute(' SELECT * FROM user WHERE email=%s', (data['email'],))
  res = jsonFormat(cursor)

  return res

def validEmail(email):
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(regex, email):
        return True
    return False

@auth.route('/clear')
def clear():
  session.clear()
  return "Clearing session!", 200

@auth.route('/check')
def check():
  return jsonify(session), 200