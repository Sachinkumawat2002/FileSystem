from django.core.mail import send_mail
from django.conf import settings
def send_email(emails):
    subject = "This email is from django server "
    message = "Tins is a test message from django server"
    from_email = "kumawatsachin720@gmail.com"
    recipient_list = [emails]
    send_mail(subject , message , from_email , recipient_list)
