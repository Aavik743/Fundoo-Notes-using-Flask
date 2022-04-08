import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_restful_swagger import swagger

from db.utils import connect_db
from routes import all_routes

load_dotenv()

app = Flask(__name__)
# api = Api(app)
app.config['SECRET_KEY'] = os.getenv("secret_key")
key = app.config['SECRET_KEY']
jwt = JWTManager(app)
api = swagger.docs(Api(app), apiVersion='0.1', api_spec_url='/docs')


connect_db()


def confirm_api():
    for data in all_routes:
        api_class = data[0]
        endpoint = data[1]
        api.add_resource(api_class, endpoint)


confirm_api()

if __name__ == '__main__':
    app.run(debug=True)
