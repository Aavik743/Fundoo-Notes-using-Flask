import base64
from datetime import timedelta

from flask_jwt_extended import decode_token, create_access_token


def get_token(id):
    encoded_token = create_access_token(identity=id, expires_delta=timedelta(minutes=60000))
    return encoded_token


def data_from_token(encoded_token):
    decoded_data = decode_token(encoded_token)
    return decoded_data


def short_token(token):
    token_string_bytes = token.encode("ascii")

    base64_bytes = base64.b64encode(token_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string


def original_token(short_token):
    base64_bytes = short_token.encode("ascii")

    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")

    return sample_string
