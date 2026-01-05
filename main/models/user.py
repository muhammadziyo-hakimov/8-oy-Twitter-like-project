from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from main.utils import generate_code

import uuid


NEW, VERIFIED, DONE = ('New', 'Verified', 'Done')

class User(AbstractUser):
    status_choices = [
        (NEW, NEW),
        (VERIFIED, VERIFIED),
        (DONE, DONE),
    ]

    phone = models.CharField(max_length=13, unique=True, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=status_choices, default=NEW)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)

    def __str__(self):
        return self.username
    
    def create_code(self):
        code = generate_code()
        UserConfirmation.objects.create(user=self, code=code)
        return code
    
    def save(self, *args, **kwargs):
        if not self.username:
            user_uuid = str(uuid.uuid4()).split('-')[-1]
            self.username = f'user-{user_uuid}'
        if not self.password:
            pwd_uuid = str(uuid.uuid4()).split('-')[-1]
            self.password = f'password-{pwd_uuid}'
        super().save(*args, **kwargs)

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }



class UserConfirmation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='confirmations')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        self.expired_at = timezone.now() + timezone.timedelta(minutes=2)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expired_at
    
    def __str__(self):
        return f'{self.user.username} - {self.code}'