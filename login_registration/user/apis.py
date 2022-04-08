import json

from flask import request, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from common.exception import NotUniqueException, NotFoundException, NotMatchingException
from common import logger, utils
from .models import Users
from .utils import get_token
from flask_restful_swagger import swagger


class Register_API(Resource):
    def post(self):
        """
            This api is for user registration to this application
            @param request: user registration data like username, email, password
            @return: account verification link to registered email once registration is successful
        """
        data = json.loads(request.data)
        email_id = data.get('email_id')
        username = data.get('username')
        name = data.get('name')
        password = data.get('password')

        user = Users(name=name, username=username, password=password, email_id=email_id)
        try:
            if Users.check_username(username) or Users.check_email(email_id):
                raise NotUniqueException('user already exists', 400)
            else:
                token = get_token(user.id)
                email = email_id
                template = render_template('activation.html', token=token)
                utils.send_mail(email, template)
                user.save()
                return {'message': 'confirmation email sent', 'status code': 200, 'token': token}
        except NotUniqueException as exception:
            logger.logging.error('Log Error Message')
            return exception.__dict__
        except:
                logger.logging.error('Log Error Message')
                return {'Error': 'Something went wrong', 'status code': 500}


class ActivateAccount_API(Resource):
    @jwt_required()
    def get(self):
        """
            This Api verifies the user-id and jwt token sent to the email and activates the account
            @param request: Get request hits with jwt token which contains user information
            @return: Account activation confirmation
        """
        try:
            decoded_data = get_jwt_identity()
            print(decoded_data)
            if decoded_data:
                user = Users.objects(id=decoded_data)
                user.update(is_active=True)
            return {'message': 'account activated', 'status code': 200}
        except:
            return {'error': 'Token is missing or expired', 'status code': 400}


class Login_API(Resource):
    def post(self):
        """
            This API is used to authenticate user to access resources
            @param request: user credential like username and password
            @return: Returns success message and access token on successful login
        """
        data = json.loads(request.data)
        user_name = data.get('username')
        password = data.get('password')

        user = Users.objects.get(username=user_name)
        try:
            if password != user.password:
                raise NotMatchingException('password does not match', 400)
            if password == user.password:
                access_token = get_token(user.id)
                return {
                    'message': 'Logged in as {}'.format(data['username']),
                    'access_token': access_token
                }
            else:
                logger.logging.warning('Log Error Message')
                return {'Warning': 'Wrong Username or Password', 'status code': 400}
        except NotMatchingException as exception:
            logger.logging.error('Log Error Message')
            return exception.__dict__


class Reset_Password_API(Resource):
    @swagger.model
    @swagger.operation(notes='swagger is working')
    @jwt_required()
    def get(self):
        """
            This API accepts the changes the current password
            @param : current password and new password
            @return: success message and new password
        """
        data = json.loads(request.data)
        decoded_data = get_jwt_identity()
        password = data.get('password')
        password1 = data.get('password1')
        password2 = data.get('password2')

        user = Users.objects.get(id=decoded_data)
        try:
            if user.password != password:
                raise NotFoundException('password does not match', 400)
            if password1 != password2:
                raise NotMatchingException('new passwords does not match', 400)
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
        except NotFoundException as exception:
            logger.logging.error('Log Error Message')
            return exception.__dict__
        except NotMatchingException as exception:
            logger.logging.error('Log Error Message')
            return exception.__dict__
        except:
            logger.logging.error('Log Error Message')
            return {'Error': 'Something went wrong', 'status code': 500}


class Forgot_Pass_API(Resource):
    def get(self):
        """
            This API accepts the get request hit from the email on clicked on link
            @param : email and token
            @return: success message
        """
        data = json.loads(request.data)
        email_id = data.get('email_id')
        user = Users.objects.get(email_id=email_id)
        try:
            if not user:
                raise NotFoundException('account not available', 400)
            token = get_token(user.id)

            if user:
                email = email_id
                template = render_template('forgotpassword.html', token=token)
                utils.send_mail(email, template)

                return {"message": "forgot password link sent", 'status code': 200}

        except NotFoundException as e:
            logger.logging.error('Log Error Message')
            return e.__dict__
        except Exception as e:
            logger.logging.error('Log Error Message')
            return {'error': e, 'status code': 400}
