'''
Making code with celery 
'''

from time import sleep
from celery import shared_task


@shared_task
def notify_customer(message):
    print('sending ')
    print(message)
    sleep(10)
    print('success')
