import re
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings


email_regex =re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
phone_regex = re.compile(r"(\+[0-9]+\s*)?(\([0-9]+\))?[\s0-9\-]+[0-9]+")
username_regex = re.compile(r"^[a-zA-Z0-9_.-]+$")


def check_email_or_phone(email_or_phone):
    if re.fullmatch(email_regex, email_or_phone):
        email_or_phone = "email"

    elif re.fullmatch(phone_regex, email_or_phone):
        email_or_phone = "phone"
    else:
        data = {
            'success':False,
            "message":"email yoki raqamingiz noto'g'ri"
        }
        raise ValidationError(data)
    return email_or_phone


def check_email_username_or_phone(user_input):

    if re.fullmatch(email_regex, user_input):
        user_input = "email"

    elif re.fullmatch(phone_regex, user_input):
        user_input = "phone"
    
    elif re.fullmatch(username_regex, user_input):
        user_input = "username"

    else:
        data = {
            'success':False,
            "message":"Email, Username yoki raqamingiz noto'g'ri"
        }
        raise ValidationError(data)
    return user_input


def send_email(email, code):
    subject = 'Send email verify code'
    message = f'Salom sizning freelacer tasdiqlash kodingiz {code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email,]

    send_mail(subject, message, from_email, recipient_list)
