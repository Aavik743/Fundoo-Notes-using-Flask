import os
import smtplib
from email.message import EmailMessage


def send_mail(email):
    # EMAIL_ADDRESS = os.environ.get('aavik743@gmail.com')
    # EMAIL_PASS = os.environ.get('*****')
    #
    # msg = EmailMessage()
    # msg['Subject'] = 'Fundoo Note'
    # msg['From'] = EMAIL_ADDRESS
    # msg['To'] = email
    # msg.set_content(f"{message}")
    #
    # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # server.login(EMAIL_ADDRESS, EMAIL_PASS)
    # server.send_message(msg)
    # server.quit()

    sender = 'aavik743@gmail.com'
    receivers = email

    message = """From: From Person <from@fromdomain.com>
        Subject: Fundoo Note

        Click on the link.
        """

    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message)
