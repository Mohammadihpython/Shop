from time import sleep

from celery import shared_task
from celery.schedules import crontab
from celery.task import task, periodic_task
from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

User = get_user_model()


@shared_task(name='Send email verification link')
def send_remember_password_code(email, code):
    print('*' * 5, 'code is: ', code, '*' * 5)
    send_mail(
        "Recovery Email Password",
        'Hi, Your recovery password is: {}'.format(code),
        EMAIL_HOST_USER,
        ['{}'.format(email)],
        fail_silently=False
    )
    print('*' * 5, 'code is: ', code, '*' * 5)
