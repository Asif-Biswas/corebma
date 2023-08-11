from django.db import models
from django.contrib.auth.models import User

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
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='media/profile_pics', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    def get_friends(self):
        return self.friends.all()
    
    def get_friends_count(self):
        return self.friends.all().count()
    
    def get_posts_count(self):
        return self.posts.all().count()
    
    def get_all_authors_posts(self):
        return self.posts.all()
    
    def get_likes_given_count(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'Like':
                total_liked += 1
        return total_liked
    
    def get_likes_received_count(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked