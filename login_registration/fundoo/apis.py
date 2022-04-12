import redis
from flask import json, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from common import logger
from flask_restful_swagger import swagger
from common.exception import NotFoundException, InternalServerException, NotMatchingException
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
        """
            This API is used to create a note for user
            @param request: It takes note title, description, label(optional)
            @return: creates not on successful validation
        """
        user_id = get_jwt_identity()
        data = json.loads(request.data)
        title = data.get('title')
        description = data.get('description')
        label_id = data.get('label_id')

        data_validation = validate_create_note(data)
        if data_validation:
            return data_validation
        notes = Notes(title=title, description=description, user_id=user_id, label_id=label_id)
        try:
            if notes:
                notes.save()
                logger.logging.info('note created')
                return {'message': 'note created', 'status code': 200}
        except:
            logger.logging.info('note not created')
            return {'error': 'note not created', 'status code': 400}
        else:
            logger.logging.info('Some error occurred')
            return {'error': 'Something went wrong', 'status code': 500}

    @swagger.model
    @swagger.operation(notes='This API is used to fetch all notes of the user')
    @jwt_required()
    def get(self):
        """
            This API is used to fetch all notes of the user
            @return: returns all notes
        """
        user_notes = []
        user_id = get_jwt_identity()
        key = f"getuser{user_id}"
        value = r.get(key)
        if value:
            data = json.loads(value)
            return data

        notes = Notes.objects.filter(user_id=user_id)
        try:
            if not notes:
                raise InternalServerException('Something went wrong', 400)

            for note in notes:
                notes_ = Notes.objects.filter(isPinned=True, isTrash=False)
                for note in notes_:
                    dict_itr = note.to_dict()
                    user_notes.append(dict_itr)
                _notes = Notes.objects.filter(isPinned=False, isTrash=False)
                for note in _notes:
                    dict_itr = note.to_dict()
                    user_notes.append(dict_itr)
            logger.logging.info('notes displayed')
            do_cache(key, user_notes, 300)
            return {'redis key': key, user_id: user_notes, 'status code': 200}
        except InternalServerException as exception:
            logger.logging.info('Some error occurred')
            return exception.__dict__


class NoteFunctionalityAPI(Resource):

    @jwt_required()
    def patch(self, id):
        """
            This API is used to update the existing note
            @param request: title, description
            @param note_id: primary_key of the specific note
            @return: updates the note
         """
        user_id = get_jwt_identity()

        data = json.loads(request.data)
        title_updated = data.get('title_updated')
        description_updated = data.get('description_updated')

        notes = Notes.objects.get(id=id)
        try:
            if notes:

                if notes['user_id'] == user_id:
                    notes['title'] = title_updated
                    notes['description'] = description_updated

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
                raise NotFoundException('Note not found', 400)
        except NotFoundException as exception:
            logger.logging.info('Some error occurred')
            return exception.__dict__

    @jwt_required()
    def delete(self, id):
        """
            This API is used to delete and trash existing note
            @param note_id: primary_key of the specific note
            @return: trash or delete the note if it is already trashed
        """
        user_id = get_jwt_identity()
        notes = Notes.objects.get(id=id)
        try:
            if notes['user_id'] == user_id:
                data_validation = validate_is_trash(id)
                if data_validation:
                    return data_validation

                notes.delete()
                logger.logging.info('note deleted')
                return {'message': 'note deleted'}
            raise NotFoundException('Note not found', 400)
        except NotFoundException as exception:
            logger.logging.info('Some error occurred')
            return exception.__dict__

    @swagger.model
    @swagger.operation(notes='This API is used to fetch a notes by note id')
    @jwt_required()
    def get(self, id):
        """
            This API is used to fetch a notes by note id
            @param note_id: primary_key of the specific note
            @return: returns the note if it exist and belongs to the user
        """
        user_id = get_jwt_identity()
        notes = Notes.objects.get(id=id)
        try:
            if notes['user_id'] == user_id:
                raise InternalServerException('This note does not belong to you', 400)
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
        except InternalServerException as exception:
            logger.logging.info('Some error occurred')
            return exception.__dict__


class PinNoteApi(Resource):
    @jwt_required()
    def post(self, id):
        """
            This API is used to pin a notes by note id
            @param note_id: primary_key of the specific note
            @return: pins the note
        """
        user_id = get_jwt_identity()
        notes = Notes.objects.get(id=id)

        try:
            if not notes:
                raise NotFoundException('Could not find the note', 400)

            if notes['user_id'] == user_id:
                notes['isPinned'] = True

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
        except NotFoundException as e:
                logger.logging.info('Some error occurred')
                return e.__dict__


class TrashNoteApi(Resource):
    @jwt_required()
    def post(self, id):
        """
            This API is used to trash a notes by note id
            @param note_id: primary_key of the specific note
            @return: trashes the note
        """
        user_id = get_jwt_identity()
        notes = Notes.objects.get(id=id)
        try:
            if not notes:
                raise NotFoundException('Could not find the note', 400)
            if notes['user_id'] == user_id:
                notes['isTrash'] = True

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
        except NotFoundException as e:
            logger.logging.info('Some error occurred')
            return e.__dict__


class LabelNoteAPI(Resource):
    @jwt_required()
    def post(self, id):
        """
            This API is used to add a note to a label
            @param request: label id
            @return: adds label id to the note
        """
        data = json.loads(request.data)
        label_id = data.get('label_id')
        lb = Label.objects.filter(id=label_id).first()
        user_id = get_jwt_identity()
        notes = Notes.objects.get(id=id)
        try:
            if notes[user_id] != user_id:
                raise NotMatchingException('Users ids does not match', 400)
            if notes['user_id'] == user_id:

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
        except NotMatchingException as e:
            logger.logging.info('Some error occurred')
            return e.__dict__
