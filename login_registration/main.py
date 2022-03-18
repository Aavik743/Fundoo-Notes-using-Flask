from flask import Flask, request, jsonify, make_response
from mongoengine import connect
import model 
from flask_restful import Resource, Api
import json

connect(host="mongodb://127.0.0.1:27017/system")

app = Flask(__name__)
api = Api(app)


class Register(Resource):
    def post(self):
        data = json.loads(request.data)
        print(data)
        email_id = data.get('email_id')
        username = data.get('username')
        name = data.get('name')
        password = data.get('password')
        user = model.Users(name=name, username=username, password=password, email_id=email_id)
        print(model.Users.check_username(username))
        # users = Users.objects.get()
        # check_username = Users.query.filter_by(username='username').first()
        # check_mail = Users.query.filter_by(email_id='email').first()

        # validator db.users.find_one({"email": user["email"]})
        if model.Users.check_username(username) or model.Users.check_email(email_id):
            return make_response(jsonify(message="user already exists")), 401
        else:
            user.save()
            print(user)
            return make_response(jsonify(message="user registered")), 201


class Login(Resource):
    def post(self):
        data = json.loads(request.data)
        user_name = data.get('username')
        # user = Users.objects.get(username=user_name)
        user = model.Users.objects.filter(username=user_name)
        user_list = []
        for i in user:
            print(i.to_dict())
            user_list.append(i.to_dict())
        print(user)
        return {'message': 'success', "users": user_list}


api.add_resource(Register, '/register')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(debug=True)
