from flask import request, json
from flask_restful import Resource

from common import logger
from .models import Label
from .validators import validate_add_label, validate_if_label_exists
from flask_jwt_extended import get_jwt_identity, jwt_required


class Label_API(Resource):
    @jwt_required()
    def post(self):
        data = json.loads(request.data)
        decoded_data = get_jwt_identity()
        user_id = decoded_data
        label = data.get('label')
        validate_data = validate_add_label(data)
        if validate_data:
            return validate_data
        lb = Label(label=label, user_id=user_id)
        try:
            lb.save()
            logger.logging.info('label added')
            return {'message': 'label added', 'status code': 200}
        except:
            logger.logging.info('Some error occurred')
            return {'error': 'something went wrong', 'status code': 400}

    @jwt_required()
    def get(self):
        user_labels = []
        user_id = get_jwt_identity()
        labels = Label.objects.filter(user_id=user_id)
        try:
            for label in labels:
                dict_itr = label.to_dict()
                user_labels.append(dict_itr)
            logger.logging.info('notes displayed')
            return {user_id: user_labels, 'status code': 200}
        except:
            logger.logging.info('Some error occurred')
            return {'error': 'something went wrong', 'status code': 400}


class LabelFunctionalityAPI(Resource):
    def delete(self, id):
        validate_data = validate_if_label_exists(id)
        if validate_data:
            return validate_data
        lb = Label.objects.get(id=id)
        try:
            lb.delete()
            return {'message': 'label deleted', 'status code': 200}
        except:
            logger.logging.info('Some error occurred')
            return {'error': 'something went wrong', 'status code': 400}

    @jwt_required()
    def patch(self, id):
        data = json.loads(request.data)
        updated_label = data.get('updated_label')
        validate_data = validate_if_label_exists(id)
        if validate_data:
            return validate_data
        lb = Label.objects.get(id=id)
        lb['label'] = updated_label
        try:
            lb.save()
            return {
                'label': lb['label'],
                'status code': 200
            }
        except:
            logger.logging.info('Some error occurred')
            return {'error': 'something went wrong', 'status code': 400}

    @jwt_required()
    def get(self, id):
        validate_data = validate_if_label_exists(id)
        try:
            if validate_data:
                return validate_data
            lb = Label.objects.get(id=id)
            return {
                'id': lb['id'],
                'label': lb['label'],
                'user_id': lb['user_id']
            }
        except:
            logger.logging.info('Some error occurred')
            return {'error': 'something went wrong', 'status code': 400}
