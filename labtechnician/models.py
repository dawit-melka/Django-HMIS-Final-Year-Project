from django.db import models

from django.db import models
from django.contrib.auth.models import User


class LabTechnicianProfile(models.Model):
    labtechnician = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 20, null=True)
    last_name = models.CharField(max_length = 20, null=True)
    phone =  models.CharField(max_length=20,unique = True)
    profile_picture = models.ImageField(null=True, blank = True, upload_to = 'images/')
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name
    
class ProfileTestResult(models.Model):
    order = models.OneToOneField('doctor.LabOrder', on_delete=models.CASCADE)
    labtechnician = models.ForeignKey(LabTechnicianProfile,null=True,on_delete=models.CASCADE)
    G2000 = models.CharField(max_length = 20, null =True, blank=True)
    G2000_x = models.CharField(max_length = 20, null =True, blank=True)
    GT9 = models.CharField(max_length = 20, null =True, blank=True)
    GTI = models.CharField(max_length = 20, null =True, blank=True)
    NEO = models.CharField(max_length = 20, null =True, blank=True)
    ES = models.DecimalField(max_digits=10, decimal_places=10, null =True, blank=True)
    HB3 = models.CharField(max_length = 20, null =True, blank=True)
    DFS = models.CharField(max_length = 20, null =True, blank=True)
    LFT = models.DecimalField(max_digits=10, decimal_places=10, null =True, blank=True)
    RFT = models.DecimalField(max_digits=10, decimal_places=10,null =True, blank=True)
    TFT = models.DecimalField(max_digits=10, decimal_places=10, null =True, blank=True)
    MAC = models.CharField(max_length = 20, null =True, blank=True)
    LGL  = models.CharField(max_length = 20, null =True, blank=True)
    LIP  = models.DecimalField(max_digits=10, decimal_places=10,null =True, blank=True)

    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

class BiochemistryTestResult(models.Model):
    order = models.OneToOneField('doctor.LabOrder', on_delete=models.CASCADE)
    labtechnician = models.ForeignKey(LabTechnicianProfile,null=True,on_delete=models.CASCADE)
    CEA  = models.DecimalField(max_digits=10, decimal_places=10,null =True, blank=True)
    CA1 = models.CharField(max_length = 20, null =True, blank=True)
    CA5 = models.CharField(max_length = 20, null =True, blank=True)
    CA9 = models.CharField(max_length = 20, null =True, blank=True)
    PSA  = models.DecimalField(max_digits=10, decimal_places=10, null =True, blank=True)
    AFP  = models.DecimalField(max_digits=10, decimal_places=10,null =True, blank=True)
    Glucose  = models.DecimalField(max_digits=10, decimal_places=10, null =True, blank=True)
    HIV1_2 = models.CharField(max_length = 20, null =True, blank=True)
    HbA1c = models.DecimalField(max_digits=10, decimal_places=10,null =True, blank=True)
    HBsAg = models.CharField(max_length = 20, null =True, blank=True)
    H_pylori = models.CharField(max_length = 20, null =True, blank=True)
    Uric_Acid  = models.DecimalField(max_digits=10, decimal_places=10, null =True, blank=True)
    Free_T4 = models.DecimalField(max_digits=10, decimal_places=10, null =True, blank=True)

    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    
class HematologyResult(models.Model):
    order = models.OneToOneField('doctor.LabOrder', on_delete=models.CASCADE)
    labtechnician = models.ForeignKey(LabTechnicianProfile,null=True,on_delete=models.CASCADE)
    FBE   = models.DecimalField(max_digits=10, decimal_places=10,null =True, blank=True)
    FBC   = models.DecimalField(max_digits=10, decimal_places=10,null =True, blank=True)
    Hb   = models.DecimalField(max_digits=10, decimal_places=10,null =True, blank=True)
    Platelets   = models.IntegerField(null =True, blank=True)
    TWDC   = models.IntegerField(null =True, blank=True)
    ABO_Rh  = models.CharField(max_length = 20,null =True, blank=True)
    Malaria  = models.CharField(max_length = 20,null =True, blank=True)

    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

class MicrobiologyResult(models.Model):
    order = models.OneToOneField('doctor.LabOrder', on_delete=models.CASCADE)
    labtechnician = models.ForeignKey(LabTechnicianProfile,null=True,on_delete=models.CASCADE)
    Urine_FEME = models.DecimalField(max_digits=10, decimal_places=10,null =True, blank=True)
    RPR = models.CharField(max_length =20,null =True, blank=True)
    Microscopy = models.CharField(max_length =20,null =True, blank=True)
    AFB_ZN    = models.CharField(max_length =20,null =True, blank=True)
    AFB   = models.CharField(max_length =20,null =True, blank=True)

    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

class AnatomicalPathologyResult(models.Model):
    order = models.OneToOneField('doctor.LabOrder', on_delete=models.CASCADE)
    labtechnician = models.ForeignKey(LabTechnicianProfile,null=True,on_delete=models.CASCADE)
    Histology = models.TextField(null =True, blank=True)
    Non_Gynae = models.TextField(null =True, blank=True)
  
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)