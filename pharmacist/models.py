from django.db import models
from django.contrib.auth.models import User


class PharmacistProfile(models.Model):
    pharmacist = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 20, null=True)
    last_name = models.CharField(max_length = 20, null=True)
    phone =  models.CharField(max_length=20,unique = True)
    profile_picture = models.ImageField(null=True, blank = True, upload_to = 'images/')
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name
