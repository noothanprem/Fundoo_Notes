from django.core.mail import EmailMultiAlternatives
from pyee import BaseEventEmitter
from fundoo.setting.development import EMAIL_HOST_USER

ee = BaseEventEmitter()


@ee.on('send_mail')
def send_mail(recipient_email, mail_message):
    print("Inside event emitter")
    subject = 'hello'
    from_email = EMAIL_HOST_USER
    to = recipient_email
    text_content = 'This is an important message.'
    html_content = mail_message
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
    print("mail sent")
