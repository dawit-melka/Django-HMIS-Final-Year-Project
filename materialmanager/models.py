from django.db import models
from django.contrib.auth.models import User
import datetime

YEAR_CHOICES = []
for r in range(1980, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))

condition = [
    ('operable and in service' , 'operable and in service'),
    ('operable and out of service' , 'operable and out of service'),
    ('needs maintenace' , 'needs maintenance'),
    ('not repairable' , 'not repairable')
]


class MaterialManagerProfile(models.Model):
    material_manager = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 20, null=True)
    last_name = models.CharField(max_length = 20, null=True)
    phone =  models.CharField(max_length=20,unique = True)
    profile_picture = models.ImageField(null=True, blank = True, upload_to = 'images/')
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

class Manuals(models.Model):
    manual_type = models.CharField(max_length=20) 

    def __str__(self):
        return self.manual_type


class Inventory(models.Model):
    registered_by = models.ForeignKey(MaterialManagerProfile , null=True, on_delete=models.CASCADE)
    inventory_number = models.CharField(max_length=20,primary_key=True )
    equipment_name = models.CharField(max_length=30, null=True)
    equipment_type = models.CharField(max_length=30, null=True)
    clinical_department = models.CharField(max_length=100, null=True)
    manufacturer = models.CharField(max_length=30, null=True)
    model = models.CharField(max_length=30, null=True)
    serial_number = models.CharField(max_length=30, null=True, blank=True)
    country_of_origin = models.CharField(max_length=30, null=True)
    year_of_manufacture = models.IntegerField(('Year of Manufacture'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    warranty_expired_date = models.DateField(blank=True, null=True)
    power_requirment = models.IntegerField()
    spare_parts_available = models.BooleanField(default=False)
    manuals_available = models.ManyToManyField(Manuals,blank=True)
    manual_file = models.FileField(null=True,blank=True, upload_to='manuals/') 
    dispose  = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

class InventoryRelocation(models.Model):
    inventory = models.ForeignKey(Inventory,null=True,on_delete=models.CASCADE)
    relocation_department = models.CharField(max_length=30, null=True)
    location = models.CharField(max_length=30, null=True)
    department_contact_person = models.CharField(max_length=20)
    phonenumber = models.CharField(max_length=20)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

class InvetoryStatus(models.Model):
    inventory = models.OneToOneField(Inventory,null=True,on_delete=models.CASCADE)
    condition = models.CharField(max_length=30, choices=condition)
    reason = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

class ServiceHistory(models.Model):
    material_manager = models.ForeignKey(MaterialManagerProfile, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100, null=True)
    service_description = models.TextField(null=True, blank=True)
    start_at = models.DateField(null=True)
    end_at = models.DateField(null=True)
    service_cost = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    

