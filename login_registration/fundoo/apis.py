import redis
from flask import json, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from common import logger
from common.utils import do_cache
from label.models import Label
from .models import Notes
from .validators import validate_create_note, validate_note_exists, validate_is_trash

r = redis.Redis(
    host='localhost',
    port=6379
)


class NoteAPI(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = json.loads(request.data)
        title = data.get('title')
        description = data.get('description')

        data_validation = validate_create_note(data)
        if data_validation:
            return data_validation
        notes = Notes(title=title, description=description, user_id=user_id)

        if notes:
            try:
                notes.save()
                logger.logging.info('note created')
                return {'message': 'note created', 'status code': 200}
            except:
                logger.logging.info('note not created')
                return {'error': 'note not created', 'status code': 400}
        else:
            logger.logging.info('Some error occurred')
            return {'error': 'Something went wrong', 'status code': 500}

    @jwt_required()
    def get(self):
        user_notes = []
        user_id = get_jwt_identity()
        key = f"getuser{user_id}"
        value = r.get(key)
        if value:
            data = json.loads(value)
            return data

        notes = Notes.objects.filter(user_id=user_id)
        try:
            for note in notes:
                dict_itr = note.to_dict()
                user_notes.append(dict_itr)
            logger.logging.info('notes displayed')
            do_cache(key, user_notes, 300)
            return {'redis key': key, user_id: user_notes, 'status code': 200}
        except:
            logger.logging.info('Some error occurred')
            return {'error': 'Something went wrong', 'status code': 400}


class NoteFunctionalityAPI(Resource):
    @jwt_required()
    def patch(self, id):
        user_id = get_jwt_identity()

        data = json.loads(request.data)
        title_updated = data.get('title_updated')
        description_updated = data.get('description_updated')

        notes = Notes.objects.get(id=id)

        if notes['user_id'] == user_id:
            notes['title'] = title_updated
            notes['description'] = description_updated
            try:
                notes.save()
                logger.logging.info('note updated')
                return {
                    'id': notes['id'],
                    'title': notes['title'],
                    'description': notes['description'],
                    'user_id': notes['user_id'],
                    'isPinned': notes['isPinned'],
                    'isTrash': notes['isTrash'],
                    'label_id': [lb.label for lb in notes.label_id],
                    'colour': notes['colour'],
                    'date_created': str(notes['date_created'])
                }
            except:
                logger.logging.info('Some error occurred')
                return {'error': 'Something went wrong', 'code': 400}

    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()
        notes = Notes.objects.get(id=id)
        if notes['user_id'] == user_id:
            data_validation = validate_is_trash(id)
            if data_validation:
                return data_validation
            try:
                notes.delete()
                logger.logging.info('note deleted')
                return {'message': 'note deleted'}
            except:
                logger.logging.info('Some error occurred')
                return {'error': 'Something went wrong', 'code': 400}

    @jwt_required()
    def get(self, id):
        user_id = get_jwt_identity()
        notes = Notes.objects.get(id=id)
        try:
            if notes['user_id'] == user_id:
                data_validation = validate_note_exists(id)
                if data_validation:
                    return data_validation
                return {
                    'id': notes['id'],
                    'title': notes['title'],
                    'description': notes['description'],
                    'user_id': notes['user_id'],
                    'isPinned': notes['isPinned'],
                    'isTrash': notes['isTrash'],
                    'label_id': [lb.label for lb in notes.label_id],
                    'colour': notes['colour'],
                    'date_created': str(notes['date_created'])
                }
        except:
            logger.logging.info('Some error occurred')
            return {'error': 'Something went wrong', 'code': 400}


class PinNoteApi(Resource):
    @jwt_required()
    def post(self, id):
        user_id = get_jwt_identity()
        notes = Notes.objects.get(id=id)
        if notes['user_id'] == user_id:
            notes['isPinned'] = True
            try:
                notes.save()
                return {
                    'id': notes['id'],
                    'title': notes['title'],
                    'description': notes['description'],
                    'user_id': notes['user_id'],
                    'isPinned': notes['isPinned'],
                    'isTrash': notes['isTrash'],
                    'label_id': [lb.label for lb in notes.label_id],
                    'colour': notes['colour'],
                    'date_created': json.dumps(notes['date_created'])
                }
            except:
                logger.logging.info('Some error occurred')
                return {'error': 'Something went wrong', 'status code': 400}


class TrashNoteApi(Resource):
    @jwt_required()
    def post(self, id):
        user_id = get_jwt_identity()
        notes = Notes.objects.get(id=id)
        if notes['user_id'] == user_id:
            notes['isTrash'] = True
            try:
                notes.save()
                return {
                    'id': notes['id'],
                    'title': notes['title'],
                    'description': notes['description'],
                    'user_id': notes['user_id'],
                    'isPinned': notes['isPinned'],
                    'isTrash': notes['isTrash'],
                    'label_id': [lb.label for lb in notes.label_id],
                    'colour': notes['colour'],
                    'date_created': json.dumps(notes['date_created'])
                }
            except:
                logger.logging.info('Some error occurred')
                return {'error': 'Something went wrong', 'status code': 400}


class LabelNoteAPI(Resource):
    @jwt_required()
    def post(self, id):
        data = json.loads(request.data)
        label_id = data.get('label_id')
        lb = Label.objects.filter(id=label_id).first()
        user_id = get_jwt_identity()
        notes = Notes.objects.get(id=id)
        if notes['user_id'] == user_id:
            try:
                notes.update(push__label_id=lb)
                return {
                    'id': notes['id'],
                    'title': notes['title'],
                    'description': notes['description'],
                    'user_id': notes['user_id'],
                    'isPinned': notes['isPinned'],
                    'isTrash': notes['isTrash'],
                    'label_id': [lb.label for lb in notes.label_id],
                    'colour': notes['colour'],
                    'date_created': str(notes['date_created'])
                }
            except:
                logger.logging.info('Some error occurred')
                return {'error': 'something went wrong', 'status code': 400}
