# import requests
# from celery.decorators import periodic_task
# from celery.task.schedules import crontab
# from celery.utils.log import get_task_logger
#
# from fundoo.setting.development import REMINDER_URL
#
# # redisobject=RedisOperation()
# logger = get_task_logger(__name__)
#
#
# @periodic_task(run_every=(crontab(minute='*/1')),
#                name="reminder_notification_task",
#                ignore_result=True)
# def reminder_notification_task():
# ---------------------------------------
# allnotes = requests.get(all_note_url)
# for note in allnotes.data:
#     if note.reminder-time.now() > 2000:
#         set rbmq(note email)

# ---------------------------------------

# requests.get(REMINDER_URL)
# smd_response = {
#     'success':False,
#     'message':"",
#     'data':[]
# }
# print("In")
# """sends an email when feedback form is filled successfully"""
# try:
#     user_id = redis.get("loginuser")
#     print("user name : ",user_id)
#
#     logger.info("Sent email")
#     print("Inside reminder notification")
#     subject = "tash_check"
#     message = "helloooooo"
#     sender = os.getenv('EMAIL_HOST_USER')
#     reciever = os.getenv('EMAILID')
#     send_mail(subject, message, sender, [reciever])
# except Exception:
#     smd_response['message']="Exception occuredd"
#     return smd_response
# smd_response['success']=True
# smd_response['message']="success"
# return smd_response

from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from background_task import background
from .send import Periodic_Task

# Create your views here.
periodic_class_object = Periodic_Task()


@background(schedule=1)
def hello():
    email_id = "noothan627@gmail.com"
    periodic_class_object.repeating_task(email_id)
