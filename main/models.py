from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.

class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.todo
    

class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        related_name='sender')
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receiver')
    text = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    

class Conversation(models.Model):
    user_one = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_one')
    user_two = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_two')
    messages = models.ManyToManyField(Message, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_one.username + ' ' + self.user_two.username
    
    def get_last_message(self):
        if self.messages.all():
            return self.messages.all().order_by('date').last()
        return None
    
    def get_last_message_time(self):
        last_message = self.get_last_message()
        if last_message:
            return last_message.date
        return None
    
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='media/profile_pics', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    def get_conversation_with_admin(self):
        superuser = User.objects.get(is_superuser=True)
        conversation = Conversation.objects.get_or_create(
            user_one=self.user, user_two=superuser)[0]
        return conversation


class Text(models.Model):
    login_page_welcome_text = models.CharField(max_length=100, blank=True, null=True)
    login_page_text = models.CharField(max_length=100, blank=True, null=True)
    create_an_account_text = models.CharField(max_length=100, blank=True, null=True)
    signup_page_text = models.CharField(max_length=100, blank=True, null=True)
    signup_page_welcome_text = models.CharField(max_length=100, blank=True, null=True)
    signin_instead_text = models.CharField(max_length=100, blank=True, null=True)
    chat_with_admin = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to='media/logo', blank=True)

    