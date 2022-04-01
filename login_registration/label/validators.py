from label.models import Label


def validate_add_label(data):
    label = data.get('label')
    user_id = data.get('user_id')
    lb = Label.objects.filter(user_id=user_id, label=label).first()
    if lb:
        return {'error': 'label name already present'}


def validate_if_label_exists(id):
    lb = Label.objects.filter(id=id)
    if lb is None:
        return {'error': 'label does not exist'}
