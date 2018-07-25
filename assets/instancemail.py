from django.core.mail import EmailMultiAlternatives
import os
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings.configure()


class InitEmail():
    def __init__(self, namefile, subject, from_email, to, text_content, html_content):
        self.namefile = namefile
        self.subject = subject
        self.from_email = from_email
        self.to = to
        self.text_content = text_content
        self.html_content = html_content

    def readfile(self):
        global data
        with open(os.path.join(BASE_DIR, self.namefile), 'r+') as file:
            data = file.read().replace('{{linkverify}}', self.html_content)
        print(data)
        return data

    def sendemailinit(self):
        subject, from_email, to = self.subject, self.from_email, self.to
        text_content = self.text_content
        html_content = self.readfile()
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


InitEmail("assets/email.html", "Hello", 'osxunixl@gmail.com', 'htcvtc59@gmail.com',
          'datatdadadada', "https://localhost:8000/sign").sendemailinit()
