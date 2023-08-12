from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ToDoList, Message, Conversation, UserProfile
from django.db.models import Q
import json
from django.http import JsonResponse

# Create your views here.


@login_required(login_url='login')
def home(request):
    if request.user.is_superuser:
        todos = ToDoList.objects.all()
    else:
        todos = ToDoList.objects.filter(user=request.user)
    return render(request, 'main/home.html', {'todos': todos})


@login_required(login_url='login')
def add_todo(request):
    if request.method == 'POST':
        todo = request.POST.get('todo')
        user = request.user
        ToDoList.objects.create(user=user, todo=todo)
        # messages.success(request, 'Todo added successfully')
        return redirect('home')
    

@login_required(login_url='login')
def delete_todo(request, id):
    todo = ToDoList.objects.get(id=id)
    todo.delete()
    # messages.success(request, 'Todo deleted successfully')
    return redirect('home')


@login_required(login_url='login')
def complete_todo(request, id):
    # if not request.user.is_superuser:
    #     return redirect('home')
    todo = ToDoList.objects.get(id=id)
    todo.completed = True
    todo.save()
    # messages.success(request, 'Todo completed successfully')
    return redirect('home')


@login_required(login_url='login')
def incomplete_todo(request, id):
    # if not request.user.is_superuser:
    #     return redirect('home')
    todo = ToDoList.objects.get(id=id)
    todo.completed = False
    todo.save()
    # messages.success(request, 'Todo incomplete successfully')
    return redirect('home')


@login_required(login_url='login')
def conversations(request):
    conversations = Conversation.objects.filter(
        Q(user_one=request.user) | Q(user_two=request.user)).order_by('-updated')
    return render(request, 'main/conversations.html', {'conversations': conversations})


@login_required(login_url='login')
def conversation(request, id=None):
    if id:
        conversation = Conversation.objects.get(id=id)
    else:
        superuser = User.objects.get(is_superuser=True)
        conversation = Conversation.objects.get_or_create(
            user_one=request.user, user_two=superuser)[0]
        
    return render(request, 'main/chat.html', {'conversation': conversation})


@login_required(login_url='login')
def send_message(request, id):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        text = data['text']
        conversation = Conversation.objects.get(id=id)
        msg = Message.objects.create(
            sender=request.user, receiver=conversation.user_two, text=text)
        conversation.messages.add(msg)
        conversation.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})
    
    
@login_required(login_url='login')
def user_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    users = UserProfile.objects.all()
    return render(request, 'main/user_list.html', {'users': users})


@login_required(login_url='login')
def delete_user_profile(request, id):
    if not request.user.is_superuser:
        return redirect('home')
    user = UserProfile.objects.get(id=id)
    user.delete()
    return redirect('user_list')





def signup_view(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'main/signup.html')
        elif User.objects.filter(username=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'main/signup.html')
        elif len(password1) < 6:
            messages.error(request, 'Password too short')
            return render(request, 'main/signup.html')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'main/signup.html')
        else:
            user = User.objects.create_user(
                first_name=firstname, last_name=lastname, email=email, username=email, password=password1)
            user.save()
            messages.success(request, 'Account created successfully')
            return render(request, 'main/login.html')
    return render(request, 'main/signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # messages.success(request, 'Login successful')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'main/login.html')

    return render(request, 'main/login.html')


def logout_view(request):
    logout(request)
    # messages.success(request, 'Logout successful')
    return redirect('login')
