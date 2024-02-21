from django.db import models
from django.contrib.auth.models import User #Coming from django admin

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True) # Many to Many participants. Already connected to a User model, so we are using related name
    updated = models.DateTimeField(auto_now=True) #Adding many times stamps
    created = models.DateTimeField(auto_now_add=True) #Adding time stamp for just one time

    class Meta: #Using the meta data to reorder the room/topic to appear in newest order
        ordering = ['-updated', '-created']
    

    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #One to Many relationship, a user can have many messages, but not the other way around
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #If room gets deleted, cascade the messages
    body = models.TextField() #Message from the users
    updated = models.DateTimeField(auto_now=True) #Adding many times stamps
    created = models.DateTimeField(auto_now_add=True) #Adding time stamp for just one time

    class Meta: #Using the meta data to reorder the room/topic to appear in newest order
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50] #First 50 messages
