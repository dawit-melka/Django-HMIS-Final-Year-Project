from django.db import models
from django.contrib.auth.models import User

gendertype = [
        ('Male','M'),
        ('Female','F')
    ]


class NurseProfile(models.Model):
    nurse = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 20, null=True)
    last_name = models.CharField(max_length = 20, null=True)
    phone =  models.CharField(max_length=20,unique = True)
    profile_picture = models.ImageField(null=True, blank = True, upload_to = 'images/')
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

class VitalSigns(models.Model):
    Patient = models.ForeignKey('reception.Patient', null=True, on_delete=models.CASCADE)
    Nurse = models.ForeignKey(NurseProfile, null=True, on_delete=models.CASCADE)
    weight = models.IntegerField(null=True,blank=True)
    temprature = models.IntegerField(null=True,blank=True)
    pulse = models.IntegerField(null=True,blank=True)
    blood_pressure = models.CharField(max_length=20, null=True,blank=True)
    respirations = models.IntegerField(null=True,blank=True)
    bloodsugar = models.IntegerField(null=True,blank=True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
       ordering = ['-created']

class RegisterDeath(models.Model):
    Patient = models.OneToOneField('reception.Patient', null=True, on_delete=models.CASCADE)
    Nurse = models.ForeignKey(NurseProfile, null=True, on_delete=models.CASCADE)
    death_date = models.DateField(blank=True, null=True)
    death_time = models.TimeField(blank=True, null=True)
    death_reason=models.TextField(null=True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

class RegisterBirth(models.Model):
    Nurse = models.ForeignKey(NurseProfile, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 20, null=True)
    middle_name = models.CharField(max_length = 20, null=True)
    last_name = models.CharField(max_length = 20, null=True)
    gender = models.CharField(max_length=10,choices=gendertype,null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    time_of_birth = models.TimeField(blank=True, null=True)
    birth_weight = models.IntegerField()
    birth_length = models.IntegerField()
    mother_first_name = models.CharField(max_length = 20, null=True)
    mother_middle_name = models.CharField(max_length = 20, null=True)
    mother_last_name = models.CharField(max_length = 20, null=True)
    mother_date_of_birth = models.DateField(blank=True, null=True)
    mother_nationality = models.CharField(max_length = 20, null=True)
    mother_occupation = models.CharField(max_length = 20, null=True)
    father_first_name = models.CharField(max_length = 20, null=True)
    father_middle_name = models.CharField(max_length = 20, null=True)
    father_last_name = models.CharField(max_length = 20, null=True)
    father_date_of_birth = models.DateField(blank=True, null=True)
    father_nationality = models.CharField(max_length = 20, null=True)
    father_occupation = models.CharField(max_length = 20, null=True)
    address = models.CharField(null=True,max_length=20)
    region = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True,blank=True)
    phone =  models.CharField(max_length=20,unique = True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
       ordering = ['-created']