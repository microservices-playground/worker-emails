import pika
import json
import os

from jinja2 import Environment, FileSystemLoader

from EmailSender import EmailSender
from Email import Email

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
channel.exchange_declare(exchange='email', type='direct', durable=True)

queue_name = 'email'

print(' [*] Waiting for logs. To exit press CTRL+C')


def test_mail(to_email, type, context):

    env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.realpath(__file__)) + '/templates'))
    template = env.get_template('register.html')
    rendered = template.render(username=context['username']).encode('utf-8')

    email = Email(to_email, 'Subject', rendered)
    email_sender = EmailSender(env)

    email_sender.send_email(email)


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

    json_data = json.loads(body)
    email = json_data['email']
    type = json_data['type']
    context = json_data['context']

    test_mail(email, type, context)


channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()



