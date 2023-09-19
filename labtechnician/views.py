from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import RegistrationForm, LabTechnicianProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from reception.models import Patient
from doctor.models import LabOrder
from django.db.models import Q 
from administrator.models import Messaging, Announcement
from django.contrib.auth.models import User
from doctor.forms import OrderLabForm1
from .forms import ProfileTestResultForm, BiochemistryTestResultForm,HematologyResultForm,MicrobiologyResultForm,AnatomicalPathologyResultForm
from .models import ProfileTestResult, BiochemistryTestResult, HematologyResult, MicrobiologyResult, AnatomicalPathologyResult

def RegisterLabTechnician(request):
    user_form = RegistrationForm()
    labtechnician_profile_form = LabTechnicianProfileForm()
    
    if request.method == 'POST':
        labtechnician_profile_form = LabTechnicianProfileForm(request.POST, request.FILES)
        user_form = RegistrationForm(request.POST)

        if user_form.is_valid():

            user = user_form.save()

            user.groups.add(6)

            labtechnician_profile = labtechnician_profile_form.save(commit=False)
            labtechnician_profile.labtechnician = user
            labtechnician_profile.save()

            login(request,user)
            return redirect('after-login')
    return render(request,'labtechnician/register.html', {'user_form':user_form, 'profile_form' : labtechnician_profile_form , 'page': 'Lab Technician' })


@login_required(login_url='login')
def LabTechnicianHome(request):
    announcements = Announcement.objects.all()[:2]
    return render(request,'labtechnician/lab_home.html', {'announcements':announcements})

@login_required(login_url='login')
def Announcements(request):
    announcements = Announcement.objects.all()
    return render(request,'labtechnician/announcement.html',{'announcements':announcements})

def UpdateLabtechnician(request):
    profile = request.user.labtechnicianprofile
    labtechnician_profile_form = LabTechnicianProfileForm(instance=profile)
    
    if request.method == 'POST':
        labtechnician_profile_form = LabTechnicianProfileForm(request.POST, request.FILES, instance=profile)

        if labtechnician_profile_form.is_valid():
            labtechnician_profile_form.save()
            return redirect('labtechnicianhome')
    return render(request,'labtechnician/lab_updateprofile.html', {'profile_form' : labtechnician_profile_form})


@login_required(login_url='login')
def LabOrders(request):
    laborders = LabOrder.objects.filter(status = False, payment = True)
    
    search_patient = request.GET.get('search')
    if search_patient:
        laborders = LabOrder.objects.filter(Q(Patient__first_name__icontains=search_patient) | Q(Patient__last_name__icontains=search_patient)
                                | Q(Patient__middle_name__icontains=search_patient) | Q(Patient__email__icontains=search_patient) | Q(Patient__phone__icontains=search_patient)).filter(status = False, payment = True)


    return render(request,'labtechnician/laborder.html', {'laborders':laborders})

@login_required(login_url='login')
def LabSearchPatients(request):
    search_patient = request.GET.get('search')
    
    if search_patient:
        searched_patients = Patient.objects.filter(Q(first_name__icontains=search_patient) | Q(last_name__icontains=search_patient)
                                | Q(middle_name__icontains=search_patient) | Q(email__icontains=search_patient) | Q(phone__icontains=search_patient))
    else:
        searched_patients=Patient.objects.all()

    return render(request,'labtechnician/searchpatients.html',{'patients':searched_patients})

def PatientProfile(request,pk):
    patient = Patient.objects.get(id=pk)
    laborders = LabOrder.objects.filter(Patient = patient, payment = True)
    return render(request,'labtechnician/patientprofile.html', {'patient' : patient  , 'laborders':laborders})

def LabOrderAndResults(request,pk):
    laborder = LabOrder.objects.get(id=pk)
    orderlabform = OrderLabForm1(instance=laborder)
    return render(request,'labtechnician/laborderandresults.html', {'orderlabform':orderlabform, 'laborder':laborder})

def LabOrderResultForm(request,pk):
    laborder = LabOrder.objects.get(id=pk)

    profiletestresultform = ProfileTestResultForm()
    biochemistrytestresultform = BiochemistryTestResultForm()
    hematologyresultform = HematologyResultForm()
    microbiologyresultform = MicrobiologyResultForm()
    anatomicalpathologyresultform = AnatomicalPathologyResultForm()

    if request.method == 'POST':
        profiletestresultform = ProfileTestResultForm(request.POST)
        biochemistrytestresultform = BiochemistryTestResultForm(request.POST)
        hematologyresultform = HematologyResultForm(request.POST)
        microbiologyresultform = MicrobiologyResultForm(request.POST)
        anatomicalpathologyresultform = AnatomicalPathologyResultForm(request.POST)

        if profiletestresultform.is_valid() and biochemistrytestresultform.is_valid() and hematologyresultform.is_valid() and microbiologyresultform.is_valid() and anatomicalpathologyresultform.is_valid():
            profiletestresult = profiletestresultform.save(commit=False)
            profiletestresult.order = laborder
            profiletestresult.labtechnician = request.user.labtechnicianprofile
            profiletestresult.save()

            biochemistrytestresult = biochemistrytestresultform.save(commit=False)
            biochemistrytestresult.order = laborder
            biochemistrytestresult.labtechnician = request.user.labtechnicianprofile
            biochemistrytestresult.save()

            hematologyresult = hematologyresultform.save(commit=False)
            hematologyresult.order = laborder
            hematologyresult.labtechnician = request.user.labtechnicianprofile
            hematologyresult.save()

            microbiologyresult = microbiologyresultform.save(commit=False)
            microbiologyresult.order = laborder
            microbiologyresult.labtechnician = request.user.labtechnicianprofile
            microbiologyresult.save()

            anatomicalpathologyresult = anatomicalpathologyresultform.save(commit=False)
            anatomicalpathologyresult.order = laborder
            anatomicalpathologyresult.labtechnician = request.user.labtechnicianprofile
            anatomicalpathologyresult.save()

            laborder.status = True
            laborder.save()

            return redirect('laborderresult', laborder.id)

    context = {
        'laborder':laborder,

        'profiletestresultform' : profiletestresultform,
        'biochemistrytestresultform' : biochemistrytestresultform,
        'hematologyresultform' : hematologyresultform,
        'microbiologyresultform':microbiologyresultform,
        'anatomicalpathologyresultform' : anatomicalpathologyresultform
    }
    return render(request,'labtechnician/labresultform.html', context)


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

    return render(request,'labtechnician/result.html', context)

@login_required(login_url='login')
def LabMessages(request):
   
    chats = User.objects.all()

    array = []
    staffs = User.objects.all()
    for staff in staffs:
        chatcount = Messaging.objects.filter(sender=staff, receiver=request.user, seen = False)
        array.append(chatcount.count())
    
    zipped =zip(chats,array)

    context = {'chats':chats, 'array':array, 'zipped':zipped}
    
    return render(request,"labtechnician/messages/messages_base.html", context)

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
    
        return redirect('radiologistmessagelist', pk=user.id)


    context = {'chats':chats, 'messageslist': messageslist, 'user':user, 'zipped':zipped}

    return render(request,"labtechnician/messages/messages.html", context)