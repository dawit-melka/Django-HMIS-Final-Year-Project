from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from datetime import date

class Patient(models.Model):
    bloodtype = [
    ('A', 'A'),
    ('B', 'B'),
    ('AB', 'AB'),
    ('O', 'O'),
    ]

    RHtype = [
        ('+', '+'),
        ('-', '-')
    ]

    gendertype = [
        ('Male','M'),
        ('Female','F')
    ]
    reception = models.ForeignKey(User , null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 20, null=True)
    middle_name = models.CharField(max_length = 20, null=True)
    last_name = models.CharField(max_length = 20, null=True)
    gender = models.CharField(max_length=10,choices=gendertype,null=True)
    email = models.EmailField(null=True,blank=True)
    phone =  models.CharField(max_length=20,unique = True,default=True)
    dateofbirth = models.DateField(blank=True, null=True)
    bloodtype = models.CharField(max_length=10, choices= bloodtype)
    RH = models.CharField(max_length=10, choices= RHtype)
    address = models.CharField(null=True,max_length=20)
    
    def get_age(self):
        age = date.today()-self.dateofbirth
        return int((age).days/365.25)

    def __str__(self):
        return self.first_name

class ReceptionProfile(models.Model):
    recepetion = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 20, null=True)
    last_name = models.CharField(max_length = 20, null=True)
    phone =  models.CharField(max_length=20,unique = True)
    profile_picture = models.ImageField(null=True, blank = True, upload_to = 'images/')

    def __str__(self):
        return self.first_name

class DoctorSpecalization(models.Model):
    specalization = models.CharField(max_length=40, null=True)
    
    def __str__(self):
        return self.specalization
    

class DoctorProfile(models.Model):
    doctor = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 20, null=True)
    middle_name = models.CharField(max_length = 20, null=True)
    last_name = models.CharField(max_length = 20, null=True)
    phone =  models.CharField(max_length=20,unique = True)
    Specalization = models.ForeignKey(DoctorSpecalization, null=True, on_delete=models.CASCADE)
    profile_picture = models.ImageField(null=True, blank = True, upload_to = 'images/')

    def __str__(self):
        return self.first_name

class Appointment(models.Model):
    Specalization = models.ForeignKey(DoctorSpecalization, null=True, on_delete=models.CASCADE)
    Doctor = models.ForeignKey(DoctorProfile, null=True, on_delete=models.CASCADE)
    Patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now = True)
    updated = models.DateTimeField(auto_now_add = True)

class PrescribedMedicine(models.Model):
    medicine = models.CharField(max_length = 100, null=True)
    dosage = models.CharField(max_length = 100, null=True)
    instruction = models.TextField(null=True)
    Patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE)
    Doctor = models.ForeignKey(DoctorProfile, null=True, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now = True)
    updated = models.DateTimeField(auto_now_add = True)

class LabOrder(models.Model):
    labtests = models.TextField(null=True)
    Patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE)
    Doctor = models.ForeignKey(DoctorProfile, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now = True)
    updated = models.DateTimeField(auto_now_add = True)

class MedicalHistory (models.Model):
    report = models.TextField(null=True)
    Patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE)
    Doctor = models.ForeignKey(DoctorProfile, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now = True)
    updated = models.DateTimeField(auto_now_add = True)

class PharmacistProfile(models.Model):
    pharmacist = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 20, null=True)
    last_name = models.CharField(max_length = 20, null=True)
    phone =  models.CharField(max_length=20,unique = True)
    profile_picture = models.ImageField(null=True, blank = True, upload_to = 'images/')

    def __str__(self):
        return self.first_name


