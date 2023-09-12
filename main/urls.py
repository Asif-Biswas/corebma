from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    path('add-todo/', views.add_todo, name='add_todo'),
    path('delete-todo/<int:id>/', views.delete_todo, name='delete_todo'),
    path('complete-todo/<int:id>/', views.complete_todo, name='complete_todo'),
    path('incomplete-todo/<int:id>/', views.incomplete_todo, name='incomplete_todo'),

    # conversations
    path('conversations/', views.conversations, name='conversations'),
    path('conversation/', views.conversation, name='conversation'),
    path('conversation/<int:id>/', views.conversation, name='conversation'),
    path('send-message/<int:id>/', views.send_message, name='send_message'),
    path('direct-chat/<int:id>/', views.direct_chat, name='direct_chat'),

    # user list
    path('user-list/', views.user_list, name='user_list'),
    path('delete-user-profile/<int:id>/', views.delete_user_profile, name='delete_user_profile'),


    # API
    path('home-api/', views.home_api, name='home_api'),
    path('add-todo-api/', views.add_todo_api, name='add_todo_api'),
    path('delete-todo-api/<int:id>/', views.delete_todo_api, name='delete_todo_api'),
    path('complete-todo-api/<int:id>/', views.complete_todo_api, name='complete_todo_api'),
    path('incomplete-todo-api/<int:id>/', views.incomplete_todo_api, name='incomplete_todo_api'),

    # conversations
    path('conversations-api/', views.conversations_api, name='conversations_api'),
    path('conversation-api/', views.conversation_api, name='conversation_api'),
    path('conversation-api/<int:id>/', views.conversation_api, name='conversation_api'),
    path('send-message-api/<int:id>/', views.send_message_api, name='send_message_api'),

    # user list
    path('user-list-api/', views.user_list_api, name='user_list_api'),
    path('delete-user-profile-api/<int:id>/', views.delete_user_profile_api, name='delete_user_profile_api'),

    # auth
    path('login-api/', views.login_api, name='login_api'),
    path('signup-api/', views.signup_api, name='signup_api'),
    path('logout-api/', views.logout_api, name='logout_api'),
    
    path('app/', views.home, name='test'),
    path('todo/', views.todo, name='todo'),
    path('chat/', views.chat, name='chat')
]