from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AdminProfile, Announcement
from cashier.models import CashierProfile

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = '__all__'
        exclude = ['administrator']

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = '__all__'
        exclude = ['administrator']


class DateInput(forms.DateInput):
    input_type='date'

class ExcelForm(forms.Form):
    date= forms.DateField(label='Date', widget=DateInput)

