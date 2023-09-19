from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import LabTechnicianProfile, ProfileTestResult, BiochemistryTestResult, HematologyResult, MicrobiologyResult,AnatomicalPathologyResult

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class LabTechnicianProfileForm(forms.ModelForm):
    class Meta:
        model = LabTechnicianProfile
        fields = '__all__'
        exclude = ['labtechnician','active']

class ProfileTestResultForm(forms.ModelForm):
    class Meta:
        model = ProfileTestResult
        fields = '__all__'
        exclude = ['labtechnician','order']

class BiochemistryTestResultForm(forms.ModelForm):
    class Meta:
        model = BiochemistryTestResult
        fields = '__all__'
        exclude = ['labtechnician','order']

class HematologyResultForm(forms.ModelForm):
    class Meta:
        model = HematologyResult
        fields = '__all__'
        exclude = ['labtechnician','order']

class MicrobiologyResultForm(forms.ModelForm):
    class Meta:
        model = MicrobiologyResult
        fields = '__all__'
        exclude = ['labtechnician','order']

class AnatomicalPathologyResultForm(forms.ModelForm):
    class Meta:
        model = AnatomicalPathologyResult
        fields = '__all__'
        exclude = ['labtechnician','order']