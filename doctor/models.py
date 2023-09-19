from django.db import models
from django.contrib.auth.models import User
import uuid

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
    price = models.IntegerField(default=0,null=True)
    active = models.BooleanField(default=False)
    is_working_now = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name
    
class PrescribedMedicine(models.Model):
    Cashier = models.ForeignKey('cashier.CashierProfile', null=True, on_delete=models.CASCADE)
    medicine = models.CharField(max_length = 100, null=True)
    dosage = models.CharField(max_length = 100, null=True)
    instruction = models.TextField(null=True)
    Patient = models.ForeignKey('reception.Patient', null=True, on_delete=models.CASCADE)
    Doctor = models.ForeignKey(DoctorProfile, null=True, on_delete=models.CASCADE)
    payment = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now = True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)


class ProfileTest(models.Model):
    test_type = models.CharField(max_length=10)
    price = models.IntegerField(null=True) 

    def __str__(self):
        return self.test_type
class BiochemistryTest(models.Model):
    test_type = models.CharField(max_length=10)
    price = models.IntegerField(null=True) 

    def __str__(self):
        return self.test_type
class HematologyTest(models.Model):
    test_type = models.CharField(max_length=10)
    price = models.IntegerField(null=True)  

    def __str__(self):
        return self.test_type
class MicrobiologyTest(models.Model):
    test_type = models.CharField(max_length=25) 
    price = models.IntegerField(null=True)

    def __str__(self):
        return self.test_type
    
class AnatomicalPathologyTest(models.Model):
    test_type = models.CharField(max_length=10)
    price = models.IntegerField(null=True) 

    def __str__(self):
        return self.test_type
    
class SampleType(models.Model):
    test_type = models.CharField(max_length=10) 

    def __str__(self):
        return self.test_type
class Fasting(models.Model):
    test_type = models.CharField(max_length=10)

    def __str__(self):
        return self.test_type

class LabOrder(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    Cashier = models.ForeignKey('cashier.CashierProfile', null=True, blank= True, on_delete=models.CASCADE)
    sample_type = models.ManyToManyField(SampleType,blank=True)
    fasting = models.ManyToManyField(Fasting,blank=True)
    profile_test = models.ManyToManyField(ProfileTest,blank=True)
    biochemistry_test = models.ManyToManyField(BiochemistryTest,blank=True)
    hematology_test = models.ManyToManyField(HematologyTest, blank=True)
    microbiology_test = models.ManyToManyField(MicrobiologyTest,blank=True)
    anatomical_pathology_test = models.ManyToManyField(AnatomicalPathologyTest,blank=True)
    additional_tests = models.TextField(null=True,blank=True)
    Patient = models.ForeignKey('reception.Patient', null=True, on_delete=models.CASCADE)
    Doctor = models.ForeignKey(DoctorProfile, null=True, on_delete=models.CASCADE)
    payment = models.BooleanField(default=False)
    note = models.TextField(null=True,blank=True)
    status = models.BooleanField(default=False)
    price = models.IntegerField(null=True,blank=True)
    lab = models.BooleanField(default=True)
    payment_date = models.DateTimeField(auto_now = True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
       ordering = ['-created']

    @property
    def total_price(self):
        total = 0
        total += sum(test.price for test in self.profile_test.all())
        total += sum(test.price for test in self.biochemistry_test.all())
        total += sum(test.price for test in self.hematology_test.all())
        total += sum(test.price for test in self.microbiology_test.all())
        total += sum(test.price for test in self.anatomical_pathology_test.all())
        
        return total

class ImagingType(models.Model):
    imagingtype = models.TextField(null=True)
    price = models.IntegerField(null=True)

    def __str__(self):
        return self.imagingtype


class RadiologyOrder(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    Cashier = models.ForeignKey('cashier.CashierProfile', null=True, on_delete=models.CASCADE)
    imagingtype = models.ForeignKey(ImagingType, null=True, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    Patient = models.ForeignKey('reception.Patient', null=True, on_delete=models.CASCADE)
    Doctor = models.ForeignKey(DoctorProfile, null=True, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    payment = models.BooleanField(default=False)
    radio = models.BooleanField(default=True)
    payment_date = models.DateTimeField(auto_now = True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
       ordering = ['-created']

    @property
    def total_price(self):
        total = self.imagingtype.price
        
        return total

class MedicalHistory (models.Model):
    report = models.TextField(null=True)
    Patient = models.ForeignKey('reception.Patient', null=True, on_delete=models.CASCADE)
    Doctor = models.ForeignKey(DoctorProfile, null=True, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
       ordering = ['-created']

