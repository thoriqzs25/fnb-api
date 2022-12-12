from flask import Flask
from database import mysql
from blueprints.fnb import fnb
# from blueprints.fnb import api as fnbApi
from blueprints.auth import auth
from flask_restx import Api, Resource

# from blueprints.swagger import swagger

app = Flask(__name__)
 
app.register_blueprint(auth)
app.register_blueprint(fnb)
# app.register_blueprint(swagger)

# api = Api(
#     title='Fnb API',
#     version='1.0',
# )

# api.add_namespace(fnbApi)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tubes_tst'
app.config['MYSQL_UNIX_SOCKET'] = '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
app.config["FLASK_DEBUG"] = 1

mysql.init_app(app)

# @api.route('/fnb')
# class AllFnb(Resource):
#     def get(self):
#         return 'asd'
#     def post(self):
#         return 'asd'

# @api.route('/fnb/<int:id>')
# class FnbId(Resource):
#     def get(self):
#         return 'asd'
#     def put(self):
#         return 'asd'
#     def delete(self):
        # return 'asd'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
    # app.run(debug=True)