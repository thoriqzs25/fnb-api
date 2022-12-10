import bcrypt

key = "thoriqganteng"

# ePass --> enteredPassword
# cPass --> currentPassword
def encodeStr(ePass):
  hashed_password = bcrypt.hashpw((key+ePass).encode("utf-8"), bcrypt.gensalt())
  return hashed_password

def verifyUser(ePass, cPass):
  return bcrypt.checkpw((key+ePass).encode("utf-8"), cPass.encode("utf-8"))




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
