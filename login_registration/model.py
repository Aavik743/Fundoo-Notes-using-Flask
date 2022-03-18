from mongoengine import Document, StringField, EmailField, BooleanField, DateTimeField, connect
import datetime
from main import db


class Users(Document):
    name = StringField()
    username = StringField()
    password = StringField()
    email_id = EmailField()
    is_active = BooleanField()
    dt_created = DateTimeField(default=datetime.datetime.now)
    dt_updated = DateTimeField(default=datetime.datetime.now)

    def __repr__(self):
        return 'user: {}'.format(self.username)

    def to_dict(self):
        user_dict = {
            'name': self.name,
            'username': self.username,
            'email_id': self.email_id,
            'password': self.password,
            'is_active': self.is_active,
            'dt_created': self.dt_created,
            'dt_updated': self.dt_updated
        }
        return user_dict

    @classmethod
    def check_username(cls, username):
        data1 = Users.objects.filter(username=username)
        return data1

    @classmethod
    def check_email(cls, email_id):
        return db.users.findOne({'email_id': email_id}).first()
