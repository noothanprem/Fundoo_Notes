# #!/usr/bin/env python
import pdb

import pika

#from django.conf import settings
from django_cron import CronJobBase, Schedule
# import pdb
#
import requests

class Periodic_Task:


    def repeating_task(self,email_id):
        #pdb.set_trace()
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        print("hedfwedgwrdgewgvergverg")
        channel.queue_declare(queue='hello')
        print("mail sent")
        channel.basic_publish(exchange='', routing_key='hello', body=email_id)
        print(" [x] Sent 'Hello World!'")
        connection.close()
#

# import datetime
#
# # from note.models import Notes
#
# def my_scheduled_job():
#     print(datetime.datetime.now())
#     print("fff")
#
# my_scheduled_job()