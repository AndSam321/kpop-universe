from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomForm(ModelForm): #inheriting from modelform
    class Meta: #Meta Data
        model = Room 
        fields= '__all__' #Creating form meta data from class Room
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
