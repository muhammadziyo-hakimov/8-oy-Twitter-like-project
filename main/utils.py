from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
import random
import string

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