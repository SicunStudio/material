# -*-coding:utf-8 -*-

""" email module docstring
"""

from threading import Thread
from flask_mail import Message

from material import mail, app


def send_async_email(msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body):
    """
    Args:
        subject: 主题
        recipients: 收件人的list
        text_body： 内容
        sender: 发件人，默认为配置中的发件人
    """
    MAIL = app.config['MAIL']

    message = Message(subject, sender=MAIL, recipients=recipients)
    message.html = text_body
    thread = Thread(target=send_async_email, args=[message])
    thread.start()
