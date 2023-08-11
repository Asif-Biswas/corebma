from django.contrib import admin
from .models import ToDoList, Message, Conversation, UserProfile

# Register your models here.
admin.site.register(ToDoList)
admin.site.register(Message)
admin.site.register(Conversation)
admin.site.register(UserProfile)