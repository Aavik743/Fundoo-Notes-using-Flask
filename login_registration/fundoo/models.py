import datetime

from mongoengine import StringField, SequenceField, Document, IntField, BooleanField, DateTimeField, \
    ListField, ReferenceField, PULL

from label.models import Label


class Notes(Document):
    id = SequenceField(primary_key=True)
    title = StringField()
    description = StringField()
    user_id = IntField()
    isPinned = BooleanField(default=False)
    isTrash = BooleanField(default=False)
    label_id = ListField(ReferenceField(Label, reverse_delete_rule=PULL))
    colour = StringField(default='black')
    date_created = DateTimeField(default=datetime.datetime.now)

    def to_dict(self):
        todo_dict = {
            'id': self.id,
            'topic': self.title,
            'description': self.description,
            'user_id': self.user_id,
            'isPinned': self.isPinned,
            'isTrash': self.isTrash,
            'label_id': [lb.label for lb in self.label_id],
            'colour': self.colour,
            'date_created': str(self.date_created)
        }
        return todo_dict
