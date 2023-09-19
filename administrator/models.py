from django.db import models
from django.contrib.auth.models import User

class Messaging(models.Model):
    sender = models.ForeignKey(User,null=True,on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User,null=True,on_delete=models.CASCADE, related_name='receiver')
    seen = models.BooleanField(default=False)
    body = models.CharField(max_length = 20, null=True)
    created = models.DateTimeField(auto_now = True)
    updated = models.DateTimeField(auto_now_add = True)

class AdminProfile(models.Model):
    administrator = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 20, null=True)
    last_name = models.CharField(max_length = 20, null=True)
    phone =  models.CharField(max_length=20,unique = True)
    profile_picture = models.ImageField(null=True, blank = True, upload_to = 'images/')

    def __str__(self):
        return self.first_name
    
class Announcement(models.Model):
    administrator = models.ForeignKey(AdminProfile,null=True,on_delete=models.CASCADE)
    title = models.CharField(max_length = 100, null=True)
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now = True)

    class Meta:
       ordering = ['-created']
       
    def __str__(self):
        return self.title
    