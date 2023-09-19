from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DoctorProfile, PrescribedMedicine, LabOrder ,MedicalHistory, BiochemistryTest,ProfileTest,HematologyTest,MicrobiologyTest,AnatomicalPathologyTest,SampleType,Fasting,RadiologyOrder
from reception.models import Appointment


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = '__all__'
        exclude = ['doctor','active','is_working_now','price']

class PrescribeForm(forms.ModelForm):
    class Meta:
        model = PrescribedMedicine
        feilds = '__all__'
        exclude = ['Patient','Doctor','payment','status','Cashier']

class RadiologyForm(forms.ModelForm):
    class Meta:
        model = RadiologyOrder
        feilds = '__all__'
        exclude = ['Patient','Doctor','payment','Cashier','status','Cashier','radio']

class OrderLabForm(forms.ModelForm):
    profile_test = forms.ModelMultipleChoiceField(
        queryset=ProfileTest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    biochemistry_test = forms.ModelMultipleChoiceField(
        queryset=BiochemistryTest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    hematology_test = forms.ModelMultipleChoiceField(
        queryset=HematologyTest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    microbiology_test = forms.ModelMultipleChoiceField(
        queryset=MicrobiologyTest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    anatomical_pathology_test = forms.ModelMultipleChoiceField(
        queryset=AnatomicalPathologyTest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    sample_type = forms.ModelMultipleChoiceField(
        queryset=SampleType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    fasting = forms.ModelMultipleChoiceField(
        queryset=Fasting.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = LabOrder
        feilds = 'sample_type,fasting,profile_test, biochemistry_test,hematology_test,microbiology_test,anatomical_pathology_test '
        exclude = ['Patient','Doctor','payment']
    
    

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        feilds = '__all__'
        exclude = ['Patient','Doctor']

class DateInput(forms.DateInput):
    input_type='date'

class TimeInput(forms.TimeInput):
    input_type='time'


class BookAppointmentfromProfileForm(forms.ModelForm):
    date= forms.DateField(label='appointment Date?', widget=DateInput)
    time= forms.TimeField(label='appointment Time?', widget=TimeInput)

    class Meta:
        model = Appointment
        feilds = '__all__'
        exclude = ['status','Patient','Specalization','Doctor', 'Cashier', 'payment']


class OrderLabForm1(forms.ModelForm):
    profile_test = forms.ModelMultipleChoiceField(
        queryset=ProfileTest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    biochemistry_test = forms.ModelMultipleChoiceField(
        queryset=BiochemistryTest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    hematology_test = forms.ModelMultipleChoiceField(
        queryset=HematologyTest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    microbiology_test = forms.ModelMultipleChoiceField(
        queryset=MicrobiologyTest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    anatomical_pathology_test = forms.ModelMultipleChoiceField(
        queryset=AnatomicalPathologyTest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    sample_type = forms.ModelMultipleChoiceField(
        queryset=SampleType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    fasting = forms.ModelMultipleChoiceField(
        queryset=Fasting.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    disabled_fields = ['profile_test', 'biochemistry_test', 'hematology_test', 'microbiology_test', 'anatomical_pathology_test', 'sample_type', 'fasting']
    class Meta:
        model = LabOrder
        feilds = 'sample_type,fasting,profile_test, biochemistry_test,hematology_test,microbiology_test,anatomical_pathology_test '
        exclude = ['Patient','Doctor','payment']

    def __init__(self, *args, **kwargs):
        super(OrderLabForm1, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for field in self.disabled_fields:
                self.fields[field].disabled = True
        else:
            self.fields['reviewed'].disabled = True