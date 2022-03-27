from mongoengine import Document, StringField, SequenceField


class Notes(Document):
    id = SequenceField(primary_key=True)
    username = StringField()
    topic = StringField()
    description = StringField()

    def to_dict(self):
        todo_dict = {
            'id': self.id,
            'username': self.username,
            'topic': self.topic,
            'description': self.description
        }
        return todo_dict

