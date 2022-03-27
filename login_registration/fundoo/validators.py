def validate_create_note(body):
    topic = body.get('topic')
    description = body.get('description')
    if not description or not topic or not id:
        return {'Error': 'description and topic are required fields'}
