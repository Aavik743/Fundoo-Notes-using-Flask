from datetime import timedelta

from flask_jwt_extended import decode_token, create_access_token


def get_token(id):
    encoded_token = create_access_token(identity=id, expires_delta=timedelta(minutes=60000))
    return encoded_token


# def data_from_token(encoded_token):
#     decoded_data = decode_token(encoded_token)
#     return decoded_data


