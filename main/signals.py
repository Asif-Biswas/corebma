"""
if an user is created, create a profile for that user
"""
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile, Message
from django.core.mail import send_mail
from django.conf import settings
from threading import Timer



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


def send_email_to_admin(subject, message, recipient_list):
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

        
# send email to admin when a user send a message
@receiver(post_save, sender=Message)
def send_email(sender, instance, created, **kwargs):
    if created:
        try:
            superuser = instance.sender if instance.sender.is_superuser else instance.receiver
            sent_from = instance.receiver if instance.sender.is_superuser else instance.sender
            if sent_from != superuser:
                subject = 'You have a new message'
                message = f'You have a new message from {instance.sender.username}:\n\n{instance.text}'
                recipient_list = [superuser.email]
                Timer(1, send_email_to_admin, [subject, message, recipient_list]).start()
        except Exception as e:
            print(e)
            
