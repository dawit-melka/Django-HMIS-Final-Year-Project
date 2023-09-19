from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import RegistrationForm,PharmacistProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from reception.models import Patient
from django.db.models import Q 
from datetime import datetime, date
from doctor.models import PrescribedMedicine
from administrator.models import Messaging, Announcement
from django.contrib.auth.models import User


def RegisterPharmacist(request):
    user_form = RegistrationForm()
    pharmacist_profile_form = PharmacistProfileForm()
    
    if request.method == 'POST':
        pharmacist_profile_form = PharmacistProfileForm(request.POST, request.FILES)
        user_form = RegistrationForm(request.POST)

        if user_form.is_valid():

            user = user_form.save()

            user.groups.add(7)

            pharmacist_profile = pharmacist_profile_form.save(commit=False)
            pharmacist_profile.pharmacist = user
            pharmacist_profile.save()

            login(request,user)
            return redirect('after-login')
    return render(request,'pharmacist/register.html', {'user_form':user_form, 'profile_form' : pharmacist_profile_form , 'page': 'Pharmacist' })


@login_required(login_url='login')
def PharmacistHome(request):
    announcements = Announcement.objects.all()[:2]
    return render(request,'pharmacist/pharmacist_home.html', {'announcements':announcements})

@login_required(login_url='login')
def Announcements(request):
    announcements = Announcement.objects.all()
    return render(request,'pharmacist/announcement.html',{'announcements':announcements})

@login_required(login_url='login')
def PharmacistSearchPatients(request):
    search_patient = request.GET.get('search')
    
    if search_patient:
        searched_patients = Patient.objects.filter(Q(first_name__icontains=search_patient) | Q(last_name__icontains=search_patient)
                                | Q(middle_name__icontains=search_patient) | Q(email__icontains=search_patient) | Q(phone__icontains=search_patient))
    else:
        searched_patients=Patient.objects.all()

    return render(request,'pharmacist/searchpatients.html',{'patients':searched_patients})

def UpdatePharmacist(request):
    profile = request.user.pharmacistprofile
    pharmacist_profile_form = PharmacistProfileForm(instance=profile)
    
    if request.method == 'POST':
        pharmacist_profile_form = PharmacistProfileForm(request.POST, request.FILES, instance=profile)

        if pharmacist_profile_form.is_valid():
            pharmacist_profile_form.save()
            return redirect('pharmacisthome')
    return render(request,'pharmacist/pharmacist_updateprofile.html', {'profile_form' : pharmacist_profile_form})

def PrescribedMedicines(request,pk):
    patient = Patient.objects.get(id=pk)
    prescribemeds = PrescribedMedicine.objects.filter(Patient = patient, payment = True)

    if request.method == "POST":
        prescribemed_id =request.POST.get('prescribemed_id')
        prescribemed = PrescribedMedicine.objects.get(id = prescribemed_id)
        
        if prescribemed.status == False:
            prescribemed.status = True
            prescribemed.save()
        else:
            prescribemed.status = False
            prescribemed.save()
    return render(request,'pharmacist/prescribedmedicines.html', {'patient' : patient  , 'prescribemeds':prescribemeds})

@login_required(login_url='login')
def PharmacistMessages(request):

    chats = User.objects.all()

    array = []
    staffs = User.objects.all()
    for staff in staffs:
        chatcount = Messaging.objects.filter(sender=staff, receiver=request.user, seen = False)
        array.append(chatcount.count())
    
    zipped =zip(chats,array)

    context = {'chats':chats, 'array':array, 'zipped':zipped}
    
    return render(request,"pharmacist/messages/messages_base.html", context)

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
    
        return redirect('pharmacistmessagelist', pk=user.id)


    context = {'chats':chats, 'messageslist': messageslist, 'user':user, 'zipped':zipped}

    return render(request,"pharmacist/messages/messages.html", context)
