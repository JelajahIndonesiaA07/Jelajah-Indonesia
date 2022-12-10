# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class EmergencyCallItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True )
    hospital_name = models.CharField(max_length=255)
    hospital_number = models.IntegerField()
    hospital_location = models.TextField()
    
    