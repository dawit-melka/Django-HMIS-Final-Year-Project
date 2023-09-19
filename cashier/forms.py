from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from .models import CashierProfile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class CashierProfileForm(forms.ModelForm):
    class Meta:
        model = CashierProfile
        fields = '__all__'
        exclude = ['cashier','active']

class DateInput(forms.DateInput):
    input_type='date'

class ExcelForm(forms.Form):
    date= forms.DateField(label='Date', widget=DateInput)