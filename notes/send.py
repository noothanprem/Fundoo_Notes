# #!/usr/bin/env python
# import pika
#
# #from django.conf import settings
# from django_cron import CronJobBase, Schedule
# # import pdb
# #
# import requests
#
#
# class MyCronJob(CronJobBase):
#
#     RUN_EVERY_MINS = 1
#
#     schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = 'notes.my_cron_job'
#
#     def do(self):
#         print("hedfwedgwrdgewgvergverg")
#         # connection = pika.BlockingConnection(
#         #     pika.ConnectionParameters(host='localhost'))
#         # channel = connection.channel()
#         #
#         # channel.queue_declare(queue='hello')
#         # requests.get("http://localhost:8000/api/new_notification")
#         # print("mail sent")
#         # channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
#         # #requests.get("http://localhost:8000/api/new_notification")
#         # print(" [x] Sent 'Hello World!'")
#         # connection.close()
#

import datetime

# from note.models import Notes

def my_scheduled_job():
    print(datetime.datetime.now())
    print("fff")

my_scheduled_job()