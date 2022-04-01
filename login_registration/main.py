from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from db.utils import connect_db
from routes import all_routes

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'secretkey'
key = app.config['SECRET_KEY']
jwt = JWTManager(app)


connect_db()


def confirm_api():
    for data in all_routes:
        api_class = data[0]
        endpoint = data[1]
        api.add_resource(api_class, endpoint)


confirm_api()

if __name__ == '__main__':
    app.run(debug=True)
