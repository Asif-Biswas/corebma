from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ToDoList, Message, Conversation, UserProfile
from django.db.models import Q
import json
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, ToDoListSerializer, MessageSerializer, ConversationSerializer, UserProfileSerializer
import random
# Create your views here.


# @login_required(login_url='login')
# def home(request):
#     if request.user.is_superuser:
#         todos = ToDoList.objects.all()
#     else:
#         todos = ToDoList.objects.filter(user=request.user)
#     return render(request, 'main/home.html', {'todos': todos})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home_api(request):
    if request.user.is_superuser:
        todos = ToDoList.objects.all()
    else:
        todos = ToDoList.objects.filter(user=request.user)
    serializer = ToDoListSerializer(todos, many=True)
    return Response(serializer.data)

@login_required(login_url='login')
def add_todo(request):
    if request.method == 'POST':
        todo = request.POST.get('todo')
        user = request.user
        ToDoList.objects.create(user=user, todo=todo)
        # messages.success(request, 'Todo added successfully')
        return redirect('todo')
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_todo_api(request):
    data = json.loads(request.body)
    todo = data['todo']
    user = request.user
    ToDoList.objects.create(user=user, todo=todo)
    return Response({'status': 'ok'})

@login_required(login_url='login')
def delete_todo(request, id):
    todo = ToDoList.objects.get(id=id)
    todo.delete()
    # messages.success(request, 'Todo deleted successfully')
    return redirect('todo')

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_todo_api(request, id):
    todo = ToDoList.objects.get(id=id)
    todo.delete()
    return Response({'status': 'ok'})

@login_required(login_url='login')
def complete_todo(request, id):
    # if not request.user.is_superuser:
    #     return redirect('home')
    todo = ToDoList.objects.get(id=id)
    todo.completed = True
    todo.save()
    # messages.success(request, 'Todo completed successfully')
    return redirect('todo')

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def complete_todo_api(request, id):
    todo = ToDoList.objects.get(id=id)
    todo.completed = True
    todo.save()
    return Response({'status': 'ok'})

@login_required(login_url='login')
def incomplete_todo(request, id):
    # if not request.user.is_superuser:
    #     return redirect('home')
    todo = ToDoList.objects.get(id=id)
    todo.completed = False
    todo.save()
    # messages.success(request, 'Todo incomplete successfully')
    return redirect('todo')

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def incomplete_todo_api(request, id):
    todo = ToDoList.objects.get(id=id)
    todo.completed = False
    todo.save()
    return Response({'status': 'ok'})


@login_required(login_url='login')
def conversations(request):
    conversations = Conversation.objects.filter(
        Q(user_one=request.user) | Q(user_two=request.user)).order_by('-updated')
    return render(request, 'main/v-chat.html', {'conversations': conversations})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversations_api(request):
    conversations = Conversation.objects.filter(
        Q(user_one=request.user) | Q(user_two=request.user)).order_by('-updated')
    serializer = ConversationSerializer(conversations, many=True)
    return Response(serializer.data)



def conversation(request, id=None):
    if id:
        conversation = Conversation.objects.get(id=id)
    else:
        superuser = User.objects.get(is_superuser=True)
        conversation = Conversation.objects.get_or_create(
            user_one=request.user, user_two=superuser)[0]
        
    return render(request, 'main/v-conversation.html', {'history': conversation})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversation_api(request, id=None):
    if id:
        conversation = Conversation.objects.get(id=id)
    else:
        superuser = User.objects.get(is_superuser=True)
        conversation = Conversation.objects.get_or_create(
            user_one=request.user, user_two=superuser)[0]
    messages = conversation.messages.all()
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)



def send_message(request, id):
    if request.method == 'POST':
        text = request.POST.get('text')
        conversation = Conversation.objects.get(id=id)
        if 'user' in request.session:
            user = User.objects.get(id=request.session['user'])
        else:
            user = request.user
        msg = Message.objects.create(
            sender=user, receiver=conversation.user_two, text=text)
        conversation.messages.add(msg)
        conversation.save()
        return render(request, 'main/v-chat-message-right.html', {'message': msg})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message_api(request, id):
    data = json.loads(request.body)
    text = data['text']
    conversation = Conversation.objects.get(id=id)
    msg = Message.objects.create(
        sender=request.user, receiver=conversation.user_two, text=text)
    conversation.messages.add(msg)
    conversation.save()
    return Response({'status': 'ok'})

    
@login_required(login_url='login')
def user_list(request):
    users = UserProfile.objects.all()
    return render(request, 'main/v-users.html', {'users': users})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list_api(request):
    if not request.user.is_superuser:
        return Response({'status': 'error'})
    users = UserProfile.objects.all()
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data)


@login_required(login_url='login')
def delete_user_profile(request, id):
    if not request.user.is_superuser:
        return redirect('home')
    user = UserProfile.objects.get(id=id)
    user.delete()
    return redirect('user_list')

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_profile_api(request, id):
    if not request.user.is_superuser:
        return Response({'status': 'error'})
    user = UserProfile.objects.get(id=id)
    user.delete()
    return Response({'status': 'ok'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_profile_api(request, id):
    if not request.user.is_superuser:
        return redirect('home')
    user = UserProfile.objects.get(id=id)
    user.delete()
    return Response({'status': 'ok'})


def direct_chat(request, id):
    conversations = Conversation.objects.filter(
        Q(user_one=request.user) | Q(user_two=request.user)).order_by('-updated')
    userProfile, _ = UserProfile.objects.get_or_create(user=request.user)
    conversation = Conversation.objects.get(id=id)
    context = {
        'chatPage': True,
        'conversations': conversations,
        'userProfile': userProfile,
        'history': conversation,
    }
    return render(request, 'main/v-chat.html', context)



def signup_view(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'main/auth-register-cover.html')
        elif User.objects.filter(username=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'main/auth-register-cover.html')
        elif len(password1) < 6:
            messages.error(request, 'Password too short')
            return render(request, 'main/auth-register-cover.html')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'main/auth-register-cover.html')
        else:
            user = User.objects.create_user(
                first_name=firstname, last_name=lastname, email=email, username=email, password=password1)
            user.save()
            messages.success(request, 'Account created successfully')
            return render(request, 'main/auth-login-cover.html')
    return render(request, 'main/auth-register-cover.html')

@api_view(['POST'])
def signup_api(request):
    data = json.loads(request.body)
    firstname = data['firstname']
    lastname = data['lastname']
    email = data['email']
    password1 = data['password1']
    password2 = data['password2']

    if User.objects.filter(email=email).exists():
        return Response({'status': 'error', 'message': 'Email already exists'})
    elif User.objects.filter(username=email).exists():
        return Response({'status': 'error', 'message': 'Email already exists'})
    elif len(password1) < 6:
        return Response({'status': 'error', 'message': 'Password too short'})
    elif password1 != password2:
        return Response({'status': 'error', 'message': 'Passwords do not match'})
    else:
        user = User.objects.create_user(
            first_name=firstname, last_name=lastname, email=email, username=email, password=password1)
        user.save()

        # login user
        token, created = Token.objects.get_or_create(user=user)
        return Response({'status': 'ok', 'token': token.key})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # remove session
            if 'user' in request.session:
                del request.session['user']

            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'main/auth-login-cover.html')

    return render(request, 'main/auth-login-cover.html')

@api_view(['POST'])
def login_api(request):
    data = json.loads(request.body)
    email = data['email']
    password = data['password']

    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'status': 'ok', 'token': token.key})
    else:
        return Response({'status': 'error', 'message': 'Invalid credentials'})
    

def logout_view(request):
    logout(request)
    # messages.success(request, 'Logout successful')
    return redirect('login')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    token = Token.objects.get(user=request.user)
    token.delete()
    return Response({'status': 'ok'})


@login_required(login_url='login')
def home(request):
    if request.user.is_superuser:
        todos = ToDoList.objects.all()
    else:
        todos = ToDoList.objects.filter(user=request.user)
    context = {
        'todoPage': True,
        'todos': todos,
    }
    return render(request, 'main/v_base.html', context)

def todo(request):
    if request.user.is_superuser:
        todos = ToDoList.objects.all()
    else:
        todos = ToDoList.objects.filter(user=request.user)
    context = {
        'todoPage': True,
        'todos': todos,
    }
    return render(request, 'main/v-todo.html', context)

def chat(request):
    conversations = Conversation.objects.filter(
        Q(user_one=request.user) | Q(user_two=request.user)).order_by('-updated')
    if not conversations:
        superuser = User.objects.get(is_superuser=True)
        conversation = Conversation.objects.get_or_create(
            user_one=request.user, user_two=superuser)[0]
        conversations = Conversation.objects.filter(
            Q(user_one=request.user) | Q(user_two=request.user)).order_by('-updated')
    userProfile, _ = UserProfile.objects.get_or_create(user=request.user)
    history = conversations[0]
    context = {
        'chatPage': True,
        'conversations': conversations,
        'userProfile': userProfile,
        'history': history,
    }
    return render(request, 'main/v-chat.html', context)


def chat_with_admin(request):
    # if user is logged in, redirect to chat page
    if request.user.is_authenticated:
        return redirect('chat')
    
    superuser = User.objects.get(is_superuser=True)
    # check session for user
    if 'user' in request.session:
        user = User.objects.get(id=request.session['user'])
    else:
        # if user is not logged in, create a new user & conversation with admin
        # generate random username
        username = 'user' + str(random.randint(1, 100000))
        while User.objects.filter(username=username).exists():
            username = 'user' + str(random.randint(1, 100000))
        # create user
        user = User.objects.create_user(username=username, password='password')
        user.first_name = 'Guest'
        user.last_name = 'User'
        user.save()
        # save user in session
        request.session['user'] = user.id

    # create conversation
    conversation = Conversation.objects.get_or_create(
        user_one=user, user_two=superuser)[0]
    userProfile, _ = UserProfile.objects.get_or_create(user=user)
    context = {
        'chatPage': True,
        'userProfile': userProfile,
        'history': conversation,
        'conversation': conversation,
        'myuser': user,
    }

    return render(request, 'main/chat-with-admin.html', context)
    
    