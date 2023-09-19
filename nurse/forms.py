from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from .models import NurseProfile, VitalSigns, RegisterDeath,RegisterBirth

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class NurseProfileForm(forms.ModelForm):
    class Meta:
        model = NurseProfile
        fields = '__all__'
        exclude = ['nurse', 'active']

class VitalSignsForm(forms.ModelForm):
    class Meta:
        model = VitalSigns
        fields = '__all__'
        exclude = ['Nurse','Patient']

class DateInput(forms.DateInput):
    input_type='date'

class TimeInput(forms.TimeInput):
    input_type='time'

class RegisterDeathForm(forms.ModelForm):
    patient= forms.CharField(label='Patient Id?')
    death_date= forms.DateField(label='Death Date?', widget=DateInput)
    death_time= forms.TimeField(label='Death Time?', widget=TimeInput)

    class Meta:
        model = RegisterDeath
        fields = ['patient','death_time','death_date','death_reason']
        exclude = ['Patient','Nurse']

class RegisterBirthForm(forms.ModelForm):
    date_of_birth = forms.DateField(label='Birth Date?', widget=DateInput)
    time_of_birth = forms.TimeField(label='Birth Time?', widget=TimeInput)
    father_date_of_birth = forms.DateField(label='Father Birth Date?', widget=DateInput)
    mother_date_of_birth = forms.DateField(label='Mother Birth Date?', widget=DateInput)

    class Meta:
        model = RegisterBirth
        fields = '__all__'
        exclude = ['Nurse']