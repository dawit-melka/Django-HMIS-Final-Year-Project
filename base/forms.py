from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from .models import Patient,Appointment,DoctorProfile,ReceptionProfile, PrescribedMedicine, LabOrder ,MedicalHistory,PharmacistProfile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class ReceptionProfileForm(forms.ModelForm):
    class Meta:
        model = ReceptionProfile
        fields = '__all__'
        exclude = ['recepetion']


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = '__all__'
        exclude = ['doctor']

class PharmacistProfileForm(forms.ModelForm):
    class Meta:
        model = PharmacistProfile
        fields = '__all__'
        exclude = ['pharmacist']

class DateInput(forms.DateInput):
    input_type='date'

class PatientRegistrationForm(forms.ModelForm):
    dateofbirth= forms.DateField(label='Date of Birth?', widget=DateInput)
    class Meta:
        model = Patient
        feilds ='__all__'   
        exclude = ['reception']

class TimeInput(forms.TimeInput):
    input_type='time'

class BookAppointmentForm(forms.ModelForm):
    date= forms.DateField(label='appointment Date?', widget=DateInput)
    time= forms.TimeField(label='appointment Time?', widget=TimeInput)

    class Meta:
        model = Appointment
        feilds = ['Specalization','Doctor','Patient']
        exclude = ['user','status']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Doctor'].queryset = DoctorProfile.objects.none()

        if 'Specalization' in self.data:
            try:
                Specalization_id = int(self.data.get('Specalization'))
                self.fields['Doctor'].queryset = DoctorProfile.objects.filter(Specalization_id=Specalization_id).order_by('first_name' )
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['Doctor'].queryset = self.instance.Specalization.Doctor_set.order_by('first_name') 

class BookAppointmentfromProfileForm(forms.ModelForm):
    date= forms.DateField(label='appointment Date?', widget=DateInput)
    time= forms.TimeField(label='appointment Time?', widget=TimeInput)

    class Meta:
        model = Appointment
        feilds = ['Specalization','Doctor']
        exclude = ['user','status','Patient']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Doctor'].queryset = DoctorProfile.objects.none()

        if 'Specalization' in self.data:
            try:
                Specalization_id = int(self.data.get('Specalization'))
                self.fields['Doctor'].queryset = DoctorProfile.objects.filter(Specalization_id=Specalization_id).order_by('first_name' )
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['Doctor'].queryset = self.instance.Specalization.Doctor_set.order_by('first_name') 

class PrescribeForm(forms.ModelForm):
    class Meta:
        model = PrescribedMedicine
        feilds = '__all__'
        exclude = ['Patient','Doctor']

class OrderLabForm(forms.ModelForm):
    class Meta:
        model = LabOrder
        feilds = '__all__'
        exclude = ['Patient','Doctor']

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        feilds = '__all__'
        exclude = ['Patient','Doctor']
        