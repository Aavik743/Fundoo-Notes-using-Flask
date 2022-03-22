import json
import logging

from flask import Flask, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_mail import Mail, Message
from flask_restful import Resource, Api
from mongoengine import connect

import model
from utility import get_token

connect(host="mongodb://127.0.0.1:27017/system")

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'secretkey'
key = app.config['SECRET_KEY']
jwt = JWTManager(app)
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yourId@gmail.com'
app.config['MAIL_PASSWORD'] = '*****'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

logging.basicConfig(filename="logs.txt",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class Register_API(Resource):
    def post(self):
        data = json.loads(request.data)
        email_id = data.get('email_id')
        username = data.get('username')
        name = data.get('name')
        password = data.get('password')

        user = model.Users(name=name, username=username, password=password, email_id=email_id)
        print(user)

        if model.Users.check_username(username) or model.Users.check_email(email_id):

            return {"message": "user already exists", "status code": 401}
        else:

            try:

                token = get_token(username)

                # activation mail
                msg = Message('Hello', sender='yourId@gmail.com', recipients=['someone@gmail.com'])
                msg.body = "Click on the link to activate your account"
                mail.send(msg)

                user.save()
                return {'message': 'confirmation email sent', 'code': 200, 'token': token}
            except:
                logging.error('Log Error Message')
                return {'message': 'Something went wrong', 'status code': 500}


class ActivateAccount_API(Resource):
    # @token_required
    @jwt_required()
    def get(self):
        decoded_data = get_jwt_identity()
        print(decoded_data)
        if decoded_data:
            user = model.Users.objects(username=decoded_data)
            print(user)
            user.update(is_active=True)

            # data = Users.objects(UserName=user_name).first()
            # data.update(Is_active=True)
        return {'message': 'account activated', 'code': 200}


class Login_API(Resource):
    def post(self):
        data = json.loads(request.data)
        user_name = data.get('username')
        password = data.get('password')

        user = model.Users.objects.get(username=user_name)
        try:
            if password == user.password:
                access_token = get_token(user_name)
                return {
                    'message': 'Logged in as {}'.format(data['username']),
                    'access_token': access_token
                }
            else:
                logging.warning('Log Error Message')
                return {'message': 'Wrong Username or Password'}
        except:
            logging.error('Log Error Message')
            return {'message': 'Something went wrong', 'status code': 500}


class Reset_Password_API(Resource):
    def get(self):
        data = json.loads(request.data)
        user_name = data.get('username')
        password = data.get('password')
        password1 = data.get('password1')
        password2 = data.get('password2')

        user = model.Users.objects.get(username=user_name)
        try:
            if user.password == password:
                if password1 == password2:
                    user.password = password1
                    user.save()
                    return {"message": "new password created", "new password": user.password, 'code': 201}
                else:
                    logging.warning('Log Error Message')
                    return {"message": 'new password does not match', 'code': 400}
            else:
                logging.warning('Log Error Message')
                return {"message": 'password does not match', 'code': 400}
        except:
            logging.error('Log Error Message')
            return {'message': 'Something went wrong', 'status code': 500}


class Forgot_Pass_API(Resource):
    @jwt_required()
    def get(self):
        data = get_jwt_identity()

        user = model.Users.objects.get(username=data)

        if user:
            # forgot password mail
            msg = Message('Hello', sender='yourId@gmail.com', recipients=['someone@gmail.com'])
            msg.body = "Click on the link to change your password"
            mail.send(msg)

            return {"message": "forgot password link sent", 'code': 200}

        else:

            return {'message': 'account not available', 'code': 400}


api.add_resource(Register_API, '/register')
api.add_resource(ActivateAccount_API, '/activate')
api.add_resource(Login_API, '/login')
api.add_resource(Reset_Password_API, '/reset_password')
api.add_resource(Forgot_Pass_API, '/forgot_password')

if __name__ == '__main__':
    app.run(debug=True)
