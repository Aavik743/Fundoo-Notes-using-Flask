from mongoengine import connect


def connect_db():
    connect(host="mongodb://127.0.0.1:27017/Fundoo")
    # connect(host="mongodb://127.0.0.1:27017/notes")
