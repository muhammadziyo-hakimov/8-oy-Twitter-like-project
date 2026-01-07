from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
import random
import string
import re


def is_phone(phone: str) -> bool:
    pattern = r'\+[1-9]\d{7,14}'
    return re.fullmatch(pattern, phone) is not None


def is_email(email: str) -> bool:
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.fullmatch(pattern, email) is not None


def generate_code(size=6):
    return ''.join(random.choices(string.digits, k=size))


def send_code(email:str, code:str):
    subject = 'Confirmation Code'
    message = f'Your confirmation code is: {code}'

    
    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False
    )