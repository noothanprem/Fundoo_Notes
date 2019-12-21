import json
import pdb

from celery.decorators import task
from celery.utils.log import get_task_logger
import os
import redis
from django.core.mail import send_mail
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from fundoo.setting.development import REMINDER_URL
from celery import Celery
from notes.lib.redis_function import RedisOperation
import requests
#redisobject=RedisOperation()
logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute='*/1')),
               name="reminder_notification_task",
               ignore_result = True)
def reminder_notification_task():

    requests.get(REMINDER_URL)
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

