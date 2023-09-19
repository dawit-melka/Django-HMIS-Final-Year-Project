from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from .models import Patient,Appointment,ReceptionProfile
from doctor.models import DoctorProfile
import datetime
from django.db.models import Q

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class ReceptionProfileForm(forms.ModelForm):
    class Meta:
        model = ReceptionProfile
        fields = '__all__'
        exclude = ['recepetion', 'active']

class DateInput(forms.DateInput):
    input_type='date'

class PatientRegistrationForm(forms.ModelForm):
    dateofbirth= forms.DateField(label='Date of Birth?', widget=DateInput)
    class Meta:
        model = Patient
        feilds ='__all__'   
        exclude = ['reception','id','Cashier']


class TimeInput(forms.TimeInput):
    input_type='time'

def time_choices(interval=20):
    times = []
    for hour in range(3,11):
        for minute in range(0, 60, interval):
            time_obj = datetime.time(hour, minute)
            times.append((time_obj.strftime('%H:%M'), time_obj.strftime('%H:%M')))
    return times

def is_overlapping_appointment(Doctor, date, time):
    existing_appointments = Appointment.objects.filter(
        Q(Doctor=Doctor) & Q(date=date) & Q(time=time) & Q(status=True)
    )
    return existing_appointments.exists()


class BookAppointmentForm(forms.ModelForm):
    date= forms.DateField(label='Appointment Date?', widget=DateInput)
    time = forms.ChoiceField(label='Appointment Time?', choices=time_choices())
    patientid = forms.CharField(label='Patient Id', max_length=20)

    class Meta:
        model = Appointment
        feilds = ['patientid','Specalization','Doctor', 'date', 'time']
        exclude = ['user','status','Patient','payment','Cashier']

    def clean(self):
        cleaned_data = super().clean()
        Doctor = cleaned_data.get('Doctor')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if Doctor and date and time and is_overlapping_appointment(Doctor, date, time):
            raise forms.ValidationError("There's already an appointment scheduled with this doctor at the same time.")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Doctor'].queryset = DoctorProfile.objects.none()

        if 'Specalization' in self.data:
            try:
                Specalization_id = int(self.data.get('Specalization'))
                self.fields['Doctor'].queryset = DoctorProfile.objects.filter(Specalization_id=Specalization_id).order_by('first_name' )
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk and self.instance.Doctor:
            self.fields['Doctor'].queryset = self.instance.Specalization.Doctor_set.order_by('first_name')

    def save(self, commit=True):
        instance = super(BookAppointmentForm, self).save(commit=False)
        
        # Update the date field
        selected_date = self.cleaned_data.get('date')
        if selected_date:
            instance.date = selected_date
        
        # Update the time field
        selected_time = self.cleaned_data.get('time')
        if selected_time:
            instance.time = datetime.datetime.strptime(selected_time, '%H:%M').time()

        if commit:
            instance.save()
        return instance

class BookAppointmentfromProfileForm(forms.ModelForm):
    date= forms.DateField(label='appointment Date?', widget=DateInput)
    time = forms.ChoiceField(label='Appointment Time?', choices=time_choices())

    class Meta:
        model = Appointment
        feilds = ['Specalization','Doctor']
        exclude = ['user','status','Patient','payment','Cashier']
    
    def clean(self):
        cleaned_data = super().clean()
        Doctor = cleaned_data.get('Doctor')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if Doctor and date and time and is_overlapping_appointment(Doctor, date, time):
            raise forms.ValidationError("There's already an appointment scheduled with this doctor at the same time.")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Doctor'].queryset = DoctorProfile.objects.none()

        if 'Specalization' in self.data:
            try:
                Specalization_id = int(self.data.get('Specalization'))
                self.fields['Doctor'].queryset = DoctorProfile.objects.filter(Specalization_id=Specalization_id).order_by('first_name' )
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk and self.instance.Doctor:
            self.fields['Doctor'].queryset = self.instance.Specalization.doctorprofile_set.order_by('first_name')

    def save(self, commit=True):
        instance = super(BookAppointmentfromProfileForm, self).save(commit=False)
        
        # Update the date field
        selected_date = self.cleaned_data.get('date')
        if selected_date:
            instance.date = selected_date
        
        # Update the time field
        selected_time = self.cleaned_data.get('time')
        if selected_time:
            instance.time = datetime.datetime.strptime(selected_time, '%H:%M').time()

        if commit:
            instance.save()
        return instance
 