from flask import json, request, session, jsonify
from flask_restful import Resource

from .models import Notes
from .validators import validate_create_note
from common import logger


class CreateNoteAPI(Resource):
    def post(self):
        data = json.loads(request.data)
        username = data.get('username')
        topic = data.get('topic')
        description = data.get('description')

        data_validation = validate_create_note(data)
        if data_validation is None:
            notes = Notes(username=username, topic=topic, description=description)

            if notes:
                try:
                    notes.save()
                    logger.logging.info('note created')
                    return {'message': 'note created', 'code': 200}
                except:
                    logger.logging.info('note not created')
                    return {'error': 'note not created', 'code': 400}
        else:
            logger.logging.info('Some error occurred')
            return {'error': 'Some error occurred', 'code': 500}


class GetNotesAPI(Resource):
    def get(self):
        data = json.loads(request.data)
        username = data.get('username')
        notes = Notes.objects.get(username=username)
        logger.logging.info('notes displayed')
        return {
            'username': notes['username'],
            'topic': notes['topic'],
            'description': notes['description']
        }


class UpdateNoteAPI(Resource):
    def put(self):
        data = json.loads(request.data)
        username = data.get('username')
        topic_updated = data.get('topic_updated')
        description_updated = data.get('description_updated')
        notes = Notes.objects.get(username=username)
        notes['topic'] = topic_updated
        notes['description'] = description_updated
        notes.save()
        logger.logging.info('note updated')
        return {
            'username': notes['username'],
            'topic': notes['topic'],
            'description': notes['description']
        }


class DeleteNoteAPI(Resource):
    def get(self):
        data = json.loads(request.data)
        username = data.get('username')
        notes = Notes.objects.get(username=username)
        notes.delete()
        logger.logging.info('note deleted')
        return {'message': 'note deleted'}




