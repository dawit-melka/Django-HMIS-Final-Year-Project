from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, DoctorProfileForm, PrescribeForm,MedicalHistoryForm,OrderLabForm,BookAppointmentfromProfileForm,RadiologyForm, OrderLabForm1
from reception.models import Appointment, Patient
from django.contrib.auth import authenticate, login ,logout
from datetime import datetime, date
from django.db.models import Q 
from .models import PrescribedMedicine, MedicalHistory, PrescribedMedicine, LabOrder,RadiologyOrder
from administrator.models import Messaging,Announcement
from django.contrib.auth.models import User
from radiologist.models import RadiologyResult
from labtechnician.models import ProfileTestResult, BiochemistryTestResult, HematologyResult, MicrobiologyResult, AnatomicalPathologyResult
from nurse.models import VitalSigns
from nurse.forms import VitalSignsForm

def RegisterDoctor(request):
    user_form = RegistrationForm()
    doctor_profile_form = DoctorProfileForm()

    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        doctor_profile_form = DoctorProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and doctor_profile_form.is_valid():

            user = user_form.save() 

            user.groups.add(4)

            doctor_profile = doctor_profile_form.save(commit=False)
            doctor_profile.doctor = user
            doctor_profile.save()

            login(request,user)
            return redirect('after-login')
    
    return render(request,'doctor/register.html', {'user_form':user_form, 'profile_form' : doctor_profile_form, 'page': 'Doctor' })

@login_required(login_url='login')
def DoctorHome(request):
    announcements = Announcement.objects.all()[:2]
    doctor = request.user.doctorprofile
    today = datetime.today().date()
    appointments = Appointment.objects.filter(date=today).filter(Doctor=doctor).filter(payment = True).count()
    return render(request,'doctor/doctor_home.html',{'announcements':announcements, 'appointments':appointments})

@login_required(login_url='login')
def Announcements(request):
    announcements = Announcement.objects.all()
    return render(request,'doctor/announcement.html',{'announcements':announcements})

def UpdateDoctor(request):
    profile = request.user.doctorprofile
    doctor_profile_form = DoctorProfileForm(instance=profile)
    
    if request.method == 'POST':
        doctor_profile_form = DoctorProfileForm(request.POST, request.FILES, instance=profile)

        if doctor_profile_form.is_valid():
            doctor_profile_form.save()
            return redirect('doctorhome')
    return render(request,'doctor/doctor_updateprofile.html', {'profile_form' :  doctor_profile_form})

@login_required(login_url='login')
def ScheduleCheckup(request):
    search_patient = request.GET.get('search')
    
    if search_patient:
        searched_patients = Patient.objects.filter(Q(first_name__icontains=search_patient) | Q(last_name__icontains=search_patient)
                                | Q(middle_name__icontains=search_patient) | Q(email__icontains=search_patient) | Q(phone__icontains=search_patient))
    else:
        searched_patients=Patient.objects.all()
    return render(request,'doctor/schedulecheckup.html',{'patients':searched_patients})

@login_required(login_url='login')
def BookAppointmentfromProfile(request,pk):
    patient = Patient.objects.get(id=pk)
    form = BookAppointmentfromProfileForm()

    if request.method == 'POST':
        form = BookAppointmentfromProfileForm(request.POST)

        if form.is_valid():
            bookappointment = form.save(commit=False)
            bookappointment.Patient= patient
            bookappointment.Doctor = request.user.doctorprofile
            bookappointment.Specalization = request.user.doctorprofile.Specalization
            bookappointment.save()
            return redirect('doctorpatientprofile',pk)


    return render(request,'doctor/book_appointment.html', {'form':form})

@login_required(login_url='login')
def DoctorAppointments(request):
    doctor = request.user.doctorprofile
    today = datetime.today().date()
    appointments = Appointment.objects.filter(date=today).filter(Doctor=doctor).filter(payment = True)
    
    search_patient = request.GET.get('search')
    if search_patient:
        appointments = Appointment.objects.filter(Q(Patient__first_name__icontains=search_patient) | Q(Patient__last_name__icontains=search_patient)
                                | Q(Patient__middle_name__icontains=search_patient) | Q(Patient__email__icontains=search_patient) | Q(Patient__phone__icontains=search_patient))

    if request.method == 'POST' and request.POST.get('today')=='today':
        appointments = Appointment.objects.filter(date=today).filter(Doctor=doctor).filter(payment = True)

    if request.method == 'POST' and request.POST.get('alltime')=='alltime':
        appointments = Appointment.objects.filter(Doctor=doctor).filter(payment = True)

    if request.method == 'POST' and request.POST.get('appointment_id'):
        appointment_id =request.POST.get('appointment_id')
        appointment  = Appointment.objects.get(id=appointment_id)
        if appointment.status == False:
            appointment.status=True
            appointment.save()
        else:
            appointment.status = False
            appointment.save()
    return render(request,'doctor/doctor_appointment.html', {'appointments':appointments})

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
            return redirect('patientlprescriptionhistory',pk)
    return render(request,"doctor/prescribemed.html",{'form':form})

@login_required(login_url='login')
def RadiologyOrderPage(request,pk):
    patient = Patient.objects.get(id=pk)
    form = RadiologyForm()
    next = request.POST.get('next', '/')
    if request.method == "POST": 
        form = RadiologyForm(request.POST)
        if form.is_valid():
            radiologyform = form.save(commit=False)
            radiologyform.Doctor = request.user.doctorprofile
            radiologyform.Patient = patient
            radiologyform.save()
            return redirect('patientradiologyhistory',pk)
    return render(request,"doctor/radiologyorder.html",{'form':form})

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
            orderlabform.Patient = patient
            orderlabform.save()
            for c in request.POST.getlist('profile_test'):
                orderlabform.profile_test.add(c)
            for c in request.POST.getlist('biochemistry_test'):
                orderlabform.biochemistry_test.add(c)
            for c in request.POST.getlist('hematology_test'):
                orderlabform.hematology_test.add(c)
            for c in request.POST.getlist('microbiology_test'):
                orderlabform.microbiology_test.add(c)
            for c in request.POST.getlist('anatomical_pathology_test'):
                orderlabform.anatomical_pathology_test.add(c)
            for c in request.POST.getlist('sample_type'):
                orderlabform.sample_type.add(c)
            for c in request.POST.getlist('fasting'):
                orderlabform.fasting.add(c)

            return redirect('patientlabhistory',pk)
    return render(request,"doctor/orderlab.html",{'form':form, 'patient':patient})

def LabOrderAndResults(request,pk):
    laborder = LabOrder.objects.get(id=pk)
    orderlabform = OrderLabForm1(instance=laborder)
    return render(request,'doctor/laborderandresults.html', {'orderlabform':orderlabform, 'laborder':laborder})

@login_required(login_url='login')
def LabOrderResult(request, pk):
    laborder = LabOrder.objects.get(id=pk)

    profiletestresult = ProfileTestResult.objects.get(order = laborder) 
    biochemistrytestresult = BiochemistryTestResult.objects.get(order = laborder) 
    hematologyresult = HematologyResult.objects.get(order = laborder) 
    microbiologyresult = MicrobiologyResult.objects.get(order = laborder) 
    anatomicalpathologyresult = AnatomicalPathologyResult.objects.get(order = laborder)

    context = {
        'laborder':laborder,

        'profiletestresult' : profiletestresult,
        'biochemistrytestresult' : biochemistrytestresult,
        'hematologyresult' : hematologyresult,
        'microbiologyresult':microbiologyresult,
        'anatomicalpathologyresult' : anatomicalpathologyresult
    } 

    return render(request,'doctor/labresult.html', context)

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
            return redirect('patienthistory',pk)
    return render(request,"doctor/add_medical_history.html",{'medhistoryform':medhistoryform})

@login_required(login_url='login')
def SearchPatients(request):
    search_patient = request.GET.get('search')
    
    if search_patient:
        searched_patients = Patient.objects.filter(Q(first_name__icontains=search_patient) | Q(last_name__icontains=search_patient)
                                | Q(middle_name__icontains=search_patient) | Q(email__icontains=search_patient) | Q(phone__icontains=search_patient))
    else:
        searched_patients=Patient.objects.all()
    
    return render(request,'doctor/searchpatients.html',{'patients':searched_patients})

@login_required(login_url='login')
def PatientProfile(request,pk):

    orderlabform = OrderLabForm()
    prescribeform = PrescribeForm()
    medhistoryform = MedicalHistoryForm()
    radiologyform = RadiologyForm()

    patient = Patient.objects.get(id=pk)


    return render(request,"doctor/patientprofile.html",{'patient':patient,'medhistoryform': medhistoryform, 'prescribeform':prescribeform ,'orderlabform': orderlabform, 'radiologyform':radiologyform})

@login_required(login_url='login')
def PatientHistory(request,pk):

    patient = Patient.objects.get(id=pk)
    
    medicalhistorys= MedicalHistory.objects.all()

    return render(request,"doctor/patienthistory.html",{'patient':patient,'medicalhistorys':medicalhistorys})

@login_required(login_url='login')

@login_required(login_url='login')
def VitalSignsPage(request,pk):

    patient = Patient.objects.get(id=pk)

    vitalsigns = VitalSigns.objects.filter(Patient=patient)

    return render(request,"doctor/patientvitalsigns.html",{'patient':patient , 'vitalsigns':vitalsigns})

def PatientLabHistory(request,pk):
    patient = Patient.objects.get(id=pk)

    laborders = LabOrder.objects.filter(Patient = patient)

    return render(request,"doctor/patientlabhistory.html",{'patient':patient,'laborders':laborders})

@login_required(login_url='login')
def PatientPrescriptionHistory(request,pk):

    patient = Patient.objects.get(id=pk)
    prescribemeds = PrescribedMedicine.objects.filter(Patient = patient)

    return render(request,"doctor/patientprescriptionhistory.html",{'patient':patient, 'prescribemeds':prescribemeds})

def PatientRadiologyHistory(request,pk):
    patient = Patient.objects.get(id=pk)
    radiologyorders = RadiologyOrder.objects.filter(Patient = patient)
    return render(request,'doctor/patientradiologyhistory.html', {'patient' : patient  , 'radiologyorders':radiologyorders})

def RadiologyResults(request,pk):
    radiologyorder = RadiologyOrder.objects.get(id = pk)
    radiologyresults = RadiologyResult.objects.filter(order = radiologyorder)
    return render(request,'doctor/radiologyresult.html', {'radiologyorder':radiologyorder, 'radiologyresults':radiologyresults})


@login_required(login_url='login')
def DoctorMessages(request):
   

    chats = User.objects.all()

    array = []
    staffs = User.objects.all()
    for staff in staffs:
        chatcount = Messaging.objects.filter(sender=staff, receiver=request.user, seen = False)
        array.append(chatcount.count())
    
    zipped =zip(chats,array)

    context = {'chats':chats, 'array':array, 'zipped':zipped}
    
    return render(request,"doctor/messages/messages_base.html", context)

@login_required(login_url='login')
def MessagesList(request,pk):
    user = User.objects.get(id=pk)
    messageslist = Messaging.objects.all()

    rec_chats = Messaging.objects.filter(sender=user, receiver=request.user, seen = False)
    rec_chats.update(seen=True)


    chats = User.objects.all()
    array = []
    staffs = User.objects.all()
    for staff in staffs:
        chatcount = Messaging.objects.filter(sender=staff, receiver=request.user, seen = False)
        array.append(chatcount.count())
    
    zipped =zip(chats,array)  


    if request.method == 'POST':
        body =  request.POST.get('message')
        
        chat = Messaging.objects.create(
            sender = request.user ,
            receiver = user,
            body = body
        )
    
        return redirect('doctormessagelist', pk=user.id)


    context = {'chats':chats, 'messageslist': messageslist, 'user':user, 'zipped':zipped}

    return render(request,"doctor/messages/messages.html", context)



def file_view(request, pk):
    File = RadiologyResult.objects.get(id=pk).File
    with open('File', 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
    return response