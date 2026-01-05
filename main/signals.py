# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import User, UserConfirmation


# @receiver(post_save, sender=User)
# def create_user_conf(sender, instance, created, **kwargs):
#     if created:
#         code = generate_code()
#         UserConfirmation.objects.create(user=instance, code=code)