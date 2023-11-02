from celery import Celery, shared_task

app = Celery('alzcript')
app.conf.broker_url = 'amqp://vikiedr:bb4c2d870181d2b4fc6de2c1989295ba@rabbitmq-t6uy:5672'

@app.task(name='test')  # Named task
def test(self):
    print('Testing')