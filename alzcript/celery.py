from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alzcript.settings')

app = Celery('alzcript')

app.conf.broker_url = 'amqp://vikiedr:bb4c2d870181d2b4fc6de2c1989295ba@rabbitmq-t6uy:5672'  # TODO z env
app.autodiscover_tasks()
