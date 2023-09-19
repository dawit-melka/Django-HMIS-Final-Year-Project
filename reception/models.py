from django.db import models
from django.contrib.auth.models import User
from datetime import date
from shortuuid.django_fields import ShortUUIDField
import uuid

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
    maritaltype =[
        ('maried','Maried'),
        ('single', 'Single'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed')
    ]
    Regions = [
        ('Addis Ababa', 'Addis Ababa'),
        ('Diredawa', 'Diredawa'),
        ('Tigray', 'Tigray'),
        ('Afar', 'Afar'),
        ('Amhara', 'Amhara'),
        ('Oromia', 'Oromia'),
        ('Somali', 'Somali'),
        ('Benishangul-Gumuz', 'Benishangul-Gumuz'),
        ('Gambella', 'Gambella'),
        ('Harari', 'Harari'),
        ('Sidama', 'Sidama'),
        ('SNNP', 'SNNP'),
        ('SWEP', 'South West Ethiopian People'),
    ]
    
    reception = models.ForeignKey(User , null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 20, null=True)
    middle_name = models.CharField(max_length = 20, null=True)
    last_name = models.CharField(max_length = 20, null=True)
    gender = models.CharField(max_length=10,choices=gendertype,null=True)
    marital_status = models.CharField(max_length=10, choices=maritaltype, null=True, blank=True)
    email = models.EmailField(null=True,blank=True)
    phone =  models.CharField(max_length=20,unique = True)
    dateofbirth = models.DateField(blank=True, null=True)
    bloodtype = models.CharField(max_length=10,null=True,blank=True, choices= bloodtype)
    RH = models.CharField(max_length=10, null=True,blank=True, choices= RHtype)
    address = models.CharField(null=True,max_length=20)
    region = models.CharField(max_length=20, null=True, blank=True, choices=Regions)
    city = models.CharField(max_length=20, null=True, blank=True)

    emergency_contact_name = models.CharField(max_length=40, null=True, blank=True)
    relationship = models.CharField(max_length=20, null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
       ordering = ['-created']
    
    @property
    def get_age(self):
        age = date.today()-self.dateofbirth
        return int((age).days/365.25)

    def __str__(self):
        return self.first_name
    
    @property
    def get_name(self):
        first_name = self.first_name if self.first_name else ""
        middle_name = self.middle_name if self.middle_name else ""
        last_name = self.last_name if self.last_name else ""
        return str(first_name+ " " + middle_name+ " " + last_name)
    
    @property
    def get_bloodtype(self):
        bloodtype = ""
        rh = ""
        if self.bloodtype:
            bloodtype = self.bloodtype
        if self.RH:
            rh = self.RH
        return str(bloodtype+""+rh )   
        

    @property
    def get_gender(self):
        gender = gender
        return gender
    
    @property
    def get_address(self):
        region = ""
        city = ""
        address = ""
        if self.region:
            region = self.region
        if self.city:
            city = self.city
        if self.address:
            address = self.address
        
        full_address = str(region+ ", "+ city+", "+address)
        return full_address
    
    def __str__(self):
        return self.first_name

class ReceptionProfile(models.Model):
    recepetion = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 20, null=True)
    last_name = models.CharField(max_length = 20, null=True)
    phone =  models.CharField(max_length=20,unique = True)
    profile_picture = models.ImageField(null=True, blank = True, upload_to = 'images/')
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name
    
class Appointment(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    Specalization = models.ForeignKey('doctor.DoctorSpecalization', null=True, on_delete=models.CASCADE)
    Doctor = models.ForeignKey('doctor.DoctorProfile', null=True, on_delete=models.CASCADE)
    Patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE)
    Cashier = models.ForeignKey('cashier.CashierProfile', null=True, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    reason = models.CharField(max_length=200, null=True)
    status = models.BooleanField(default=True)
    payment = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    class Meta:
       ordering = ['-created']

    @property
    def total_price(self):
        total = self.Doctor.price
        
        return total