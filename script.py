import bcrypt
import secrets
from otp import mail
from flask_mail import Message
from flask import request, session

key = 'thoriqganteng'
tokenKey = 'superdupersecretkey'
dateFormat = '%Y-%m-%dT%H:%M:%S'

# ePass --> enteredPassword
# cPass --> currentPassword
def encodeStr(ePass):
  hashed_password = bcrypt.hashpw((key+ePass).encode("utf-8"), bcrypt.gensalt())
  return hashed_password

def verifyUser(ePass, cPass):
  return bcrypt.checkpw((key+ePass).encode("utf-8"), cPass.encode("utf-8"))

def otpHandler(data):
  otp = secrets.token_hex(3)
  ses = session.get('session')
  
  payload = {
    'data': data,
    'otp': otp
  }

  if (ses):
    for item in ses:
      if (item['data'] == data):
        return "OTP already sent, please check your email!"
    ses.append(payload)
    session['session'] = ses

  else:
    session['session'] = [payload]


  msg = Message("Your OTP, Happy Coding!", recipients=[data['email']])
  msg.body = f"Your OTP is: {otp}"
  mail.send(msg)
    
  return "Successfully sending OTP request! Please check your email!"

def jsonFormatArray(cursor):
  headers = [x[0] for x in cursor.description]
  data = cursor.fetchall()

  res = []

  for item in data:
      res.append(dict(zip(headers, item)))

  return res

def jsonFormat(cursor):
  headers = [x[0] for x in cursor.description]
  data = cursor.fetchall()
  res = {}

  for item in data:
    res = (dict(zip(headers, item)))

  return res