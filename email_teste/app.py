# coding: utf-8

'''
Aplicação teste para envio de email
'''

import os
from flask import Flask
from flask_mail import Mail, Message

APP = Flask(__name__)

APP.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=os.environ.get('USER'),
    MAIL_PASSWORD=os.environ.get('PASS'),
    MAIL_DEFAULT_SENDER=os.environ.get('USER'),
))

MAIL = Mail(APP)

@APP.route("/enviar_email")
def send_email():
    '''
    Envia um email de emergência quando chamada
    '''
    message = 'To morrendo, socorro!'
    subject = 'E-mail de emergência'
    msg = Message(recipients=["yurihenrique60@hotmail.com"],
                  subject=subject,
                  body=message)
    MAIL.send(msg)
    return None
  
if __name__ == '__main__':
    APP.run(debug=True)
