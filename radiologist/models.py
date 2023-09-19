from django.db import models

from django.contrib.auth.models import User


class RadiologistProfile(models.Model):
    radiologist = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 20, null=True)
    last_name = models.CharField(max_length = 20, null=True)
    phone =  models.CharField(max_length=20,unique = True)
    profile_picture = models.ImageField(null=True, blank = True, upload_to = 'images/')
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name
    
class RadiologyResult(models.Model):
    order = models.ForeignKey('doctor.RadiologyOrder', on_delete=models.CASCADE)
    technician = models.ForeignKey(RadiologistProfile, null=True, on_delete=models.SET_NULL)
    File = models.FileField(upload_to='radiology_results/')
    description = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)