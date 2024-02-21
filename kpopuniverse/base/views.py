from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm

# Create your views here.
# rooms = [
#     {'id':1, 'name' : 'Twice Room'},
#     {'id':2, 'name' : 'BTS Room'},
#     {'id':3, 'name' : 'Test Room'}
# ]

# Creating the login page and authentication service
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated: 
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {'page' : page}
    return render(request, 'base/login_register.html', context)

# Logging out the user
def logoutUser(request):
    logout(request)
    return redirect('home')

# Creating the register page
def registerPage(request):
    form = UserCreationForm

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # Saving the form and accessing the user. If user is uppercase, make sure lowercase
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration.')
        
    return render(request, 'base/login_register.html', {'form' : form})

# Creating the home page
def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else '' # Check if the request method has something, if q exists, then it should have a parameter
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q)) # Makes sure that whatever value we have in the topic name, it should contains it Ex: Py means python

    topic = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)) # Seeing activity for only specific room


    context = {'rooms': rooms, 
               'topics' : topic, 
               'room_count' : room_count,
               'room_messages' : room_messages}
    return render(request, 'base/home.html', context)

# Creating the room
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)
    
# this method is specifying child class, set of all messages related to this room   
# What we passed in the form, passing in body from room.html
# Dynamic value messaging to be back on that page.

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


# Updating Room
@login_required(login_url='login')
def updateRoom(request, pk): #What item we are updating
    room = Room.objects.get(id=pk) #Getting room by its id
    form = RoomForm(instance=room) #Prefilled with room value
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name) # Return object or created
        room.name = request.POST.get('name')
        room.topic = request.POST.get('topic')
        room.description = request.POST.get('description')

        Room.object.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    context = {'form' : form, 'topics': topics, 'room' : room}
    return render(request, 'base/room_form.html', context)

# Deleting Room
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')
    
    if request.method == 'POST': # String value. if its a post method
        room.delete()
        return redirect('home') # Sending user to homepage
    return render(request, 'base/delete.html', {'obj' : room}) # From the template, which room are we deleting

# Delete Message
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')
    
    if request.method == 'POST': # String value. if its a post method
        message.delete()
        return redirect('home') # Sending user to homepage
    return render(request, 'base/delete.html', {'obj' : message}) # From the template, which room are we deleting

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=request.user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update-user.html', {'form' : form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics' : topics})

def activityPage(request):
    room_messages = Message.objects.all() # Getting all the messages
    return render(request, 'base/activity.html',{'room_messages' : room_messages})

