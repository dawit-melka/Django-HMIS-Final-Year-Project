from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import RadiologistProfile, RadiologyResult

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class RadiologistProfileForm(forms.ModelForm):
    class Meta:
        model = RadiologistProfile
        fields = '__all__'
        exclude = ['radiologist','active']

class ResultForm(forms.ModelForm):
    class Meta:
        model = RadiologyResult
        fields = '__all__'
        exclude = ['technician','order']