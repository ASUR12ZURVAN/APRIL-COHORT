from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class user(models.Model):
    user_name = models.CharField(max_length = 100)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=40)
    def __str__(self):
        return self.user_name
    
class call(models.Model):
    caller_number = models.CharField(max_length=40)
    call_duration = models.TimeField()
    call_instance = models.CharField(max_length=50)  #iska matlab hai ki call kab hua tha
    transcript = models.CharField(max_length=1000)
    audio_link = models.TextField()
    avg_sentiment = models.CharField(max_length=400)

    def __str__(self):
        return self.caller_number
    
class Ticket(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    created_by = models.CharField(max_length=100)
    resolved = models.BooleanField(default=  False)

    def __str__(self):
        return Ticket.title

class Lead(models.Model):
    Name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.EmailField()
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.Name