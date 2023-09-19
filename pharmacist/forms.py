from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from .models import PharmacistProfile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class PharmacistProfileForm(forms.ModelForm):
    class Meta:
        model = PharmacistProfile
        fields = '__all__'
        exclude = ['pharmacist','active']