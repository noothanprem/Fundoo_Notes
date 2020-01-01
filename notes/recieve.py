#!/usr/bin/env python
import pdb

import pika
# from django.template.loader import render_to_string
import os
from django.core.mail import send_mail
# from pyee import BaseEventEmitter
import requests

# ee = BaseEventEmitter()
# from django.core.mail import EmailMultiAlternatives
from pyee import BaseEventEmitter

# from fundoo.setting.development import EMAIL_HOST_USER

# ee = BaseEventEmitter()
#from .event_emitter2 import ee
from .lib.event_emitter import ee
# @ee.on('send_mail')
# def send_mail(recipient_email, mail_message):
#     print("Inside event emitter")
#     subject = 'hello'
#     from_email = os.getenv('EMAIL_HOST_USER')
#     to = recipient_email
#     text_content = 'This is an important message.'
#     html_content = mail_message
#     # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#     # msg.send()
#     print("mail sent")


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    subject = "Note Reminder"
    message = "hello"
    sender = os.getenv('EMAIL_HOST_USER')
    reciever = body
    print(reciever)
    # requests.get("http://localhost:8000/api/new_notification")
    ee.emit('send_mail', reciever, message)
    print("mail send")


channel.basic_consume(
    queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
