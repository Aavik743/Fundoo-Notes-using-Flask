import os
import smtplib
from datetime import timedelta
from email.message import EmailMessage
from flask import app

from flask_jwt_extended import decode_token, create_access_token




def get_token(username):
    encoded_token = create_access_token(identity=username, expires_delta=timedelta(minutes=600))
    return encoded_token


def data_from_token(encoded_token):
    decoded_data = decode_token(encoded_token)
    return decoded_data


def activation_mail(email, token, name):
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'Activate Account'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.set_content(f"Hello {name},\n Click the link to activate your account {token}")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
        smtp.send_message(msg)
