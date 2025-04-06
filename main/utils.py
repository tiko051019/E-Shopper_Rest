from django.core.mail import EmailMessage
from E_Shop_Rest.settings import EMAIL_HOST_USER

def send_email(subject,body,to,from_email = EMAIL_HOST_USER):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to = to
    )
    return email.send()