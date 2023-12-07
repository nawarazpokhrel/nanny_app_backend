from django.conf import settings
from templated_mail.mail import BaseEmailMessage


class SendActivationEmail(BaseEmailMessage):
    template_name = 'email/otp.html'
