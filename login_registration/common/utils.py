import base64
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import redis
from dotenv import load_dotenv
import os

load_dotenv()

r = redis.Redis(
    host='localhost',
    port=6379
)

password = os.getenv("password")
my_email = os.getenv("my_email")


def send_mail(email, message):
    # create message object instance
    msg = MIMEMultipart()

    # setup the parameters of the message
    passwrd = password
    msg['From'] = my_email
    msg['To'] = email
    msg['Subject'] = "Click on the link"

    # add in the message body
    msg.attach(MIMEText(message, 'html'))


    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], passwrd)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()


def do_cache(key, value, expire_time):
    json_dict = json.dumps(value)
    r.set(key, json_dict)
    r.expire(key, expire_time)


def get_cache(key):
    value = r.get(key)
    return value


def get_short_token(token):
    token_string_bytes = token.encode("ascii")

    base64_bytes = base64.b64encode(token_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string


def get_long_token(token):
    base64_bytes = token.encode("ascii")

    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")

    return sample_string
