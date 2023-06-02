from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

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