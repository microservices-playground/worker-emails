from smtplib import SMTP
import yaml


class EmailSender:

    def __init__(self, twig_environment):
        self.twig_environment = twig_environment

    def load_config(self):

        with open('../config.yml', 'r') as f:
            config_data = f.read()

        return yaml.load(config_data)

    def send_email(self, email):

        config = self.load_config()

        debuglevel = 0
        smtp = SMTP()
        smtp.set_debuglevel(debuglevel)
        smtp.connect(config['mailer']['server'], config['mailer']['port'])
        smtp.login(config['mailer']['login'], config['mailer']['password'])

        smtp.sendmail(email.msg['From'], email.msg['To'], email.msg.as_string())
        smtp.quit()
