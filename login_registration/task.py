from celery import Celery
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import smtplib
from dotenv import load_dotenv

load_dotenv()

app = Celery('task', broker="redis://localhost:6379/0", backend='redis://localhost')


@app.task()
def send_mail(email, message):
    msg = MIMEMultipart()

    passwrd = os.getenv("password")
    msg['From'] = os.getenv("my_email")
    msg['To'] = email
    msg['Subject'] = "Click on the link"

    msg.attach(MIMEText(message, 'html'))

    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    server.login(msg['From'], passwrd)

    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()
