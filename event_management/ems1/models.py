from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Event(models.Model):
    # name,description,location,startDate,endDate,status,capacity
    name=models.CharField(max_length=55,null=True)
    description=models.CharField(max_length=455)
    location=models.CharField(max_length=100)
    startDate=models.DateField()
    endDate=models.DateField()
    capacity=models.IntegerField()
    created_by =models.ForeignKey(User, on_delete=models.CASCADE,null=True)


    def __str__(self):
     return f"{self.name}"
    

class UserAccount(models.Model):
   USER_ROLE_CHOICES = [
      ('event manager','Event Manager'),
      ('attendee','Attendee'),
   ]
   user = models.OneToOneField(User,on_delete=models.CASCADE)
   user_role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES)

   def __str__(self):
      return self.user.username



class Attendee(models.Model):
   name=models.CharField(max_length=55)
   email=models.EmailField()
   phone_number=models.IntegerField()
   event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name='attendees')

   def __str__(self):
      return f"{self.name}-{self.email}-{self.phone_number}-{self.event.name}"
   

class Analytics(models.Model):
   action=models.CharField(max_length=255)
   user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
   event=models.ForeignKey(Event,on_delete=models.SET_NULL,null=True,blank=True)
   timestamp=models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return f"{self.action} by{self.user}at{self.timestamp}"