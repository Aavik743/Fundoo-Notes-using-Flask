from fundoo.models import Notes


def validate_create_note(data):
    title = data.get('title')
    description = data.get('description')
    if not description or not title:
        return {'Error': 'description and topic are required fields'}


def validate_note_exists(id):
    note = Notes.objects.filter(id=id)
    if not note:
        return {'Error': 'note not found'}


def validate_is_trash(id):
    note = Notes.objects.get(id=id)
    if not note['isTrash']:
        return {'Error': 'note not found in trash'}
