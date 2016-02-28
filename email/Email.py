from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email:

    def __init__(self, to_email, subject, html):

        self.msg = MIMEMultipart('alternative')
        self.msg['From'] = 'Foodlove <no-reply@foodlove.pl>'
        self.msg['Subject'] = subject
        self.msg['To'] = to_email
        body = MIMEText(html, 'html', 'utf-8')
        self.msg.attach(body)
