from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MaterialManagerProfile,Inventory, InventoryRelocation,ServiceHistory, Manuals

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class MaterialManagerProfileForm(forms.ModelForm):
    class Meta:
        model = MaterialManagerProfile
        fields = '__all__'
        exclude = ['material_manager','active']

class DateInput(forms.DateInput):
    input_type='date'

class RegisterMaterialForm(forms.ModelForm):
    warranty_expired_date = forms.DateField(label='Warranty Expired Date?', widget=DateInput)
    class Meta:
        model = Inventory
        fields = '__all__'
        exclude = ['registered_by', 'dispose']

class InventoryRelocationForm(forms.ModelForm):
    inventory_number = forms.CharField(max_length=20)
    class Meta:
        model = InventoryRelocation
        fields = ['inventory_number','relocation_department','location','department_contact_person','phonenumber']
        exclude = ['inventory']

class ServiceHistoryForm(forms.ModelForm):
    inventory_number = forms.CharField(max_length=20)
    start_at= forms.DateField(label='Starts at?', widget=DateInput)
    end_at = forms.DateField(label='End at?', widget=DateInput)
    class Meta:
        model = ServiceHistory
        fields = ['inventory_number', 'service_type', 'service_description', 'start_at', 'end_at','service_cost']
        exclude = ['inventory']