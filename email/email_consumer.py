import pika
import json
import os

from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, PackageLoader, FileSystemLoader

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
channel.exchange_declare(exchange='email', type='direct', durable=True)

queue_name = 'email'

print(' [*] Waiting for logs. To exit press CTRL+C')


def send_email(toEmailAddress, type, context):

    debuglevel = 0

    # Create the container (outer) email message.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'No elo, %s!' %(context['username'])
    msg['From'] = 'Nakurwiacz kodu <test@ascetic.pl>'
    msg['To'] = toEmailAddress

    with open("email/templates/register.html", "r") as myfile:
        html = myfile.read()

    print os.path.join(os.path.dirname(__file__))
    #env = Environment(loader=PackageLoader('email', 'templates'))
    env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.realpath(__file__)) + '/templates'))

    template = env.get_template('register.html')
    rendered = template.render(username=context['username']).encode('utf-8')
    body = MIMEText(rendered, 'html', 'utf-8')

    msg.attach(body)

    smtp = SMTP()
    smtp.set_debuglevel(debuglevel)
    smtp.connect('', 587)
    smtp.login('', '')

    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp.quit()
    myfile.close()


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

    json_data = json.loads(body)
    email = json_data['email']
    type = json_data['type']
    context = json_data['context']

    print email, type, context

    send_email(email, type, context)


channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()



