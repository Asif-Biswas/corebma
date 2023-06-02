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
]