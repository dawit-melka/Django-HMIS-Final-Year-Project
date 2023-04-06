from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import RegistrationForm,PatientRegistrationForm, BookAppointmentForm, DoctorProfileForm, ReceptionProfileForm,BookAppointmentfromProfileForm, PrescribeForm,MedicalHistoryForm,OrderLabForm, PharmacistProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from .models import DoctorProfile, ReceptionProfile, Appointment,Patient, MedicalHistory, LabOrder, PrescribedMedicine
from django.db.models import Q 
from datetime import datetime, date

def index(request):
    return render (request, 'base/index.html')

def RegisterDir(request):
    return render(request, 'base/registerdir.html')

###########################register########################################

def RegisterDoctor(request):
    user_form = RegistrationForm()
    doctor_profile_form = DoctorProfileForm()

    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        doctor_profile_form = DoctorProfileForm(request.POST)

        if user_form.is_valid() and doctor_profile_form.is_valid():

            user = user_form.save() 

            user.groups.add(1)

            doctor_profile = doctor_profile_form.save(commit=False)
            doctor_profile.doctor = user
            doctor_profile.save()

            login(request,user)
            return redirect('doctorhome')
    
    return render(request,'registration/register.html', {'user_form':user_form, 'profile_form' : doctor_profile_form, 'page': 'Doctor' })

def RegisterReception(request):
    user_form = RegistrationForm()
    reception_profile_form = ReceptionProfileForm()
    
    if request.method == 'POST':
        reception_profile_form = ReceptionProfileForm(request.POST)
        user_form = RegistrationForm(request.POST)

        if user_form.is_valid():

            user = user_form.save()

            user.groups.add(3)

            reception_profile = reception_profile_form.save(commit=False)
            reception_profile.recepetion = user
            reception_profile.save()

            login(request,user)
            return redirect('receptionhome')
    return render(request,'registration/register.html', {'user_form':user_form, 'profile_form' : reception_profile_form , 'page': 'Reception' })

def RegisterPharmacist(request):
    user_form = RegistrationForm()
    pharmacist_profile_form = PharmacistProfileForm()
    
    if request.method == 'POST':
        pharmacist_profile_form = PharmacistProfileForm(request.POST)
        user_form = RegistrationForm(request.POST)

        if user_form.is_valid():

            user = user_form.save()

            user.groups.add(4)

            pharmacist_profile = pharmacist_profile_form.save(commit=False)
            pharmacist_profile.pharmacist = user
            pharmacist_profile.save()

            login(request,user)
            return redirect('pharmacisthome')
    return render(request,'registration/register.html', {'user_form':user_form, 'profile_form' : pharmacist_profile_form , 'page': 'Pharmacist' })

######################## login logot ################################

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user =User.object.get(username=username)
        except:
            messages.error(request, 'username doesnt exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.groups.filter(name='Doctor').exists():
                return redirect('doctorhome')
            elif request.user.groups.filter(name='Receptionist').exists():
                return redirect('receptionhome')
            elif request.user.groups.filter(name='Pharmacist').exists():
                return redirect('pharmacisthome')
            
        
        else:
            messages.error(request, 'incorrect password')

    return render(request,'registration/login.html')

@login_required()
def LogoutPage(request):
    logout(request)
    return redirect('login')


#####################################Receptionist##############################################

@login_required(login_url='login')
def ReceptionHome(request):
    return render(request,'base/reception/reception_home.html')

@login_required(login_url='login')
def RegisterPatient(request):
    form = PatientRegistrationForm()

    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            patient_form = form.save(commit=False)
            patient_form.reception = request.user
            patient_form.save()

            return redirect('receptionhome')

    return render(request,'base/reception/register_patient.html', {'form':form})

def UpdateReception(request):
    profile = request.user.receptionprofile
    reception_profile_form = ReceptionProfileForm(instance=profile)
    
    if request.method == 'POST':
        reception_profile_form = ReceptionProfileForm(request.POST, request.FILES, instance=profile)

        if reception_profile_form.is_valid():
            reception_profile_form.save()
            return redirect('receptionhome')
    return render(request,'base/reception/reception_updateprofile.html', {'profile_form' : reception_profile_form})

@login_required(login_url='login')
def SearchPatients(request):
    search_patient = request.GET.get('search')
    
    if search_patient:
        searched_patients = Patient.objects.filter(Q(first_name__icontains=search_patient) | Q(last_name__icontains=search_patient)
                                | Q(middle_name__icontains=search_patient) | Q(email__icontains=search_patient) | Q(phone__icontains=search_patient))
    else:
        searched_patients=Patient.objects.all()

    return render(request,'base/reception/searchpatients.html',{'patients':searched_patients})


@login_required(login_url='login')
def BookAppointment(request):
    form = BookAppointmentForm()

    if request.method == 'POST':
        form = BookAppointmentForm(request.POST)

        if form.is_valid():
            form.save()


    return render(request,'base/reception/book_appointment.html', {'form':form})

@login_required(login_url='login')
def BookAppointmentfromProfile(request,pk):
    patient = Patient.objects.get(id=pk)
    form = BookAppointmentfromProfileForm()

    if request.method == 'POST':
        form = BookAppointmentfromProfileForm(request.POST)

        if form.is_valid():
            bookappointment = form.save(commit=False)
            bookappointment.Patient= patient
            bookappointment.save()


    return render(request,'base/reception/book_appointment.html', {'form':form})

def Appointments(request):
    appointments = Appointment.objects.all()
    if request.method == 'POST':
        appointment_id =request.POST.get('appointment_id')
        appointment  = Appointment.objects.get(id=appointment_id)
        if appointment.status == False:
            appointment.status=True
            appointment.save()
        else:
            appointment.status = False
            appointment.save()
    return render(request,'base/reception/appointments.html', {'appointments':appointments})

def load_Doctors(request):
    Specalization_id = request.GET.get('Specalization')
    Doctors = DoctorProfile.objects.filter(Specalization_id=Specalization_id).order_by('first_name')
    return render(request, 'base/reception/doctor_dropdown.html', {'Doctors': Doctors})

def UpdatePatient(request,pk):
    patient=Patient.objects.get(id=pk)
    form = PatientRegistrationForm(instance=patient)

    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST, request.FILES, instance=patient)

        if form.is_valid():
            form.save()


            return redirect('receptionhome')
    return render(request,'base/reception/updatepatient.html', {'form':form})



#########################################Doctor#######################################

@login_required(login_url='login')
def DoctorHome(request):
    return render(request,'base/doctor/doctor_home.html')

def UpdateDoctor(request):
    profile = request.user.doctorprofile
    doctor_profile_form = DoctorProfileForm(instance=profile)
    
    if request.method == 'POST':
        doctor_profile_form = DoctorProfileForm(request.POST, request.FILES, instance=profile)

        if doctor_profile_form.is_valid():
            doctor_profile_form.save()
            return redirect('doctorhome')
    return render(request,'base/doctor/doctor_updateprofile.html', {'profile_form' :  doctor_profile_form})


@login_required(login_url='login')
def DoctorAppointments(request):
    doctor = request.user.doctorprofile
    today = datetime.today().date()
    appointments = Appointment.objects.filter(date=today).filter(Doctor=doctor)
    
    search_patient = request.GET.get('search')
    if search_patient:
        appointments = Appointment.objects.filter(Q(Patient__first_name__icontains=search_patient) | Q(Patient__last_name__icontains=search_patient)
                                | Q(Patient__middle_name__icontains=search_patient) | Q(Patient__email__icontains=search_patient) | Q(Patient__phone__icontains=search_patient))

    if request.method == 'POST' and request.POST.get('today')=='today':
        appointments = Appointment.objects.filter(date=today).filter(Doctor=doctor)

    if request.method == 'POST' and request.POST.get('alltime')=='alltime':
        appointments = Appointment.objects.filter(Doctor=doctor)

    if request.method == 'POST' and request.POST.get('appointment_id'):
        appointment_id =request.POST.get('appointment_id')
        appointment  = Appointment.objects.get(id=appointment_id)
        if appointment.status == False:
            appointment.status=True
            appointment.save()
        else:
            appointment.status = False
            appointment.save()
    return render(request,'base/doctor/doctor_appointment.html', {'appointments':appointments})

@login_required(login_url='login')
def PrescribeMedicine(request,pk):
    patient = Patient.objects.get(id=pk)
    form = PrescribeForm()
    next = request.POST.get('next', '/')
    if request.method == "POST": 
        form = PrescribeForm(request.POST)
        if form.is_valid():
            presribeform = form.save(commit=False)
            presribeform.Doctor = request.user.doctorprofile
            presribeform.Patient = patient
            presribeform.save()
            return HttpResponseRedirect(next)
    return render(request,"base/doctor/prescribemed.html",{'form':form})

@login_required(login_url='login')
def OrderLab(request,pk):
    patient = Patient.objects.get(id=pk)
    form = OrderLabForm()
    next = request.POST.get('next', '/')
    if request.method == "POST": 
        form = OrderLabForm(request.POST)
        if form.is_valid():
            orderlabform = form.save(commit=False)
            orderlabform.Doctor = request.user.doctorprofile
            orderlabform.save()
            return HttpResponseRedirect(next)
    return render(request,"base/doctor/orderlab.html",{'form':form})

@login_required(login_url='login')
def AddMedicalHistory(request,pk):
    patient = Patient.objects.get(id=pk)
    medhistoryform = MedicalHistoryForm()
    next = request.POST.get('next', '/')
    if request.method == "POST": 
        addmedicalhistory = MedicalHistoryForm(request.POST)
        if addmedicalhistory.is_valid():
            addhistoryform = addmedicalhistory.save(commit=False)
            addhistoryform.Doctor = request.user.doctorprofile
            addhistoryform.save()
            return HttpResponseRedirect(next)
    return render(request,"base/doctor/add_medical_history.html",{'medhistoryform':medhistoryform})

#########################################pharma##############################################################
@login_required(login_url='login')
def PharmacistHome(request):
    return render(request,'base/pharmacist/pharmacist_home.html')

@login_required(login_url='login')
def PharmacistSearchPatients(request):
    search_patient = request.GET.get('search')
    
    if search_patient:
        searched_patients = Patient.objects.filter(Q(first_name__icontains=search_patient) | Q(last_name__icontains=search_patient)
                                | Q(middle_name__icontains=search_patient) | Q(email__icontains=search_patient) | Q(phone__icontains=search_patient))
    else:
        searched_patients=Patient.objects.all()

    return render(request,'base/pharmacist/searchpatients.html',{'patients':searched_patients})

def UpdatePharmacist(request):
    profile = request.user.pharmacistprofile
    pharmacist_profile_form = PharmacistProfileForm(instance=profile)
    
    if request.method == 'POST':
        pharmacist_profile_form = PharmacistProfileForm(request.POST, request.FILES, instance=profile)

        if pharmacist_profile_form.is_valid():
            pharmacist_profile_form.save()
            return redirect('pharmacisthome')
    return render(request,'base/pharmacist/pharmacist_updateprofile.html', {'profile_form' : pharmacist_profile_form})




##############################shared#########################################################################

@login_required(login_url='login')
def PatientProfile(request,pk):

    orderlabform = OrderLabForm()
    prescribeform = PrescribeForm()
    medhistoryform = MedicalHistoryForm()

    patient = Patient.objects.get(id=pk)
    prescription_history = PrescribedMedicine.objects.filter(Patient  = patient)


    if request.user.groups.filter(name='Doctor').exists():
        return render(request,"base/doctor/patientprofile.html",{'patient':patient,'medhistoryform': medhistoryform, 'prescribeform':prescribeform ,'orderlabform': orderlabform })
    
    elif request.user.groups.filter(name='Reception').exists():
        return render(request,"base/reception/patientprofile.html",{'patient':patient})
    
    elif request.user.groups.filter(name='Pharmacist').exists():
        return render(request,"base/pharmacist/patientprofile.html",{'patient':patient, 'prescription_history':prescription_history })


@login_required(login_url='login')
def SearchPatients(request):
    search_patient = request.GET.get('search')
    
    if search_patient:
        searched_patients = Patient.objects.filter(Q(first_name__icontains=search_patient) | Q(last_name__icontains=search_patient)
                                | Q(middle_name__icontains=search_patient) | Q(email__icontains=search_patient) | Q(phone__icontains=search_patient))
    else:
        searched_patients=Patient.objects.all()
    
    if request.user.groups.filter(name='Doctor').exists():
        return render(request,'base/doctor/searchpatients.html',{'patients':searched_patients})
    else:
        return render(request,'base/reception/searchpatients.html',{'patients':searched_patients})


@login_required(login_url='login')
def LabTech(request):
    return render(request,'base/lab_home.html')


