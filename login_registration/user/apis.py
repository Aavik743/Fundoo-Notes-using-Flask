import json

from flask import request, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from .models import Users
from .utils import get_token
from common import logger, utils


class Register_API(Resource):
    def post(self):
        data = json.loads(request.data)
        email_id = data.get('email_id')
        username = data.get('username')
        name = data.get('name')
        password = data.get('password')

        user = Users(name=name, username=username, password=password, email_id=email_id)

        if Users.check_username(username) or Users.check_email(email_id):

            return {"Error": "user already exists", "status code": 401}
        else:

            try:
                token = get_token(username)
                email = email_id
                utils.send_mail(email)
                user.save()
                return {'message': 'confirmation email sent', 'status code': 200, 'token': token}
            except:
                logger.logging.error('Log Error Message')
                return {'Error': 'Something went wrong', 'status code': 500}


class ActivateAccount_API(Resource):
    @jwt_required()
    def get(self):
        try:
            decoded_data = get_jwt_identity()
            if decoded_data:
                user = Users.objects(username=decoded_data)
                user.update(is_active=True)
            return {'message': 'account activated', 'status code': 200}
        except:
            return {'error': 'Token is missing or expired', 'status code': 400}


class Login_API(Resource):
    def post(self):
        data = json.loads(request.data)
        user_name = data.get('username')
        password = data.get('password')

        user = Users.objects.get(username=user_name)
        try:
            if password == user.password:
                session['logged_in'] = True
                session['user_name'] = data['user_name']
                access_token = get_token(user_name)
                return {
                    'message': 'Logged in as {}'.format(data['username']),
                    'access_token': access_token
                }
            else:
                logger.logging.warning('Log Error Message')
                return {'Warning': 'Wrong Username or Password', 'status code': 400}
        except:
            logger.logging.error('Log Error Message')
            return {'Error': 'Something went wrong', 'status code': 500}


class Reset_Password_API(Resource):
    @jwt_required()
    def get(self):
        data = json.loads(request.data)
        user_name = data.get('username')
        password = data.get('password')
        password1 = data.get('password1')
        password2 = data.get('password2')

        user = Users.objects.get(username=user_name)
        try:
            if user.password == password:
                if password1 == password2:
                    user.password = password1
                    user.save()
                    return {"message": "new password created", "new password": user.password, 'status code': 200}
                else:
                    logger.logging.warning('Log Error Message')
                    return {"Error": 'new password does not match', 'code': 400}
            else:
                logger.logging.warning('Log Error Message')
                return {"Error": 'password does not match', 'code': 400}
        except:
            logger.logging.error('Log Error Message')
            return {'Error': 'Something went wrong', 'status code': 500}


class Forgot_Pass_API(Resource):
    def get(self):
        try:
            data = json.loads(request.data)
            user_name = data.get('username')
            user = Users.objects.get(username=user_name)

            if user:
                # forgot password mail
                # msg = Message('Hello', sender='yourId@gmail.com', recipients=['someone@gmail.com'])
                # msg.body = "Click on the link to change your password"
                # mail.send(msg)

                return {"message": "forgot password link sent", 'status code': 200}

            else:
                logger.logging.warning('Log Error Message')
                return {'Error': 'account not available', 'status code': 400}
        except:
            logger.logging.error('Log Error Message')
            return {'error': 'Token is missing or expired', 'status code': 400}


class Logout_API(Resource):
    def post(self):
        session['logged_in'] = False
        return {'message': 'logged out'}
