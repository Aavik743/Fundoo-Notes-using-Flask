from mongoengine import Document, StringField, SequenceField, IntField


class Label(Document):
    id = SequenceField(primary_key=True)
    label = StringField()
    user_id = IntField()

    def to_dict(self):
        todo_dict = {
            'id': self.id,
            'label': self.label,
            'user-id': self.user_id
        }
        return todo_dict
