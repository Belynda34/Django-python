from django.db import models
from ems1.models import Event

# Create your models here.

class Vendor(models.Model):
    name=models.CharField(max_length=55)
    services_offered=models.TextField(max_length=255)
    phone_number=models.IntegerField()
    event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name='vendors')

    def __str__(self):
        return f"Vendor: {self.name} | services_offered: {self.services_offered} | phone_number: {self.phone_number} | event: {self.event}"