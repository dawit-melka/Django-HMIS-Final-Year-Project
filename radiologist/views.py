from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from .forms import RegistrationForm, RadiologistProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from reception.models import Patient
from django.db.models import Q 
from .models import RadiologistProfile, RadiologyResult
from doctor.models import RadiologyOrder
from .forms import ResultForm
from administrator.models import Messaging,Announcement
from django.contrib.auth.models import User

def RegisterRadiologist(request):
    user_form = RegistrationForm()
    radiologist_profile_form = RadiologistProfileForm()
    
    if request.method == 'POST':
        radiologist_profile_form = RadiologistProfileForm(request.POST, request.FILES)
        user_form = RegistrationForm(request.POST)

        if user_form.is_valid():

            user = user_form.save()

            user.groups.add(5)

            radiologist_profile = radiologist_profile_form.save(commit=False)
            radiologist_profile.radiologist = user
            radiologist_profile.save()

            login(request,user)
            return redirect('after-login')
    return render(request,'radiologist/register.html', {'user_form':user_form, 'profile_form' : radiologist_profile_form , 'page': 'Radiologist' })


@login_required(login_url='login')
def RadiologistHome(request):
    announcements = Announcement.objects.all()[:2]
    radiologyorders = RadiologyOrder.objects.filter(status = False, payment = True).count()
    return render(request,'radiologist/radiologist_home.html', {'announcements':announcements, 'radiologyorders':radiologyorders})

@login_required(login_url='login')
def Announcements(request):
    announcements = Announcement.objects.all()
    return render(request,'radiologist/announcement.html',{'announcements':announcements})


@login_required(login_url='login')
def RadiologistSearchPatients(request):
    search_patient = request.GET.get('search')
    
    if search_patient:
        searched_patients = Patient.objects.filter(Q(first_name__icontains=search_patient) | Q(last_name__icontains=search_patient)
                                | Q(middle_name__icontains=search_patient) | Q(email__icontains=search_patient) | Q(phone__icontains=search_patient))
    else:
        searched_patients=Patient.objects.all()

    return render(request,'radiologist/searchpatients.html',{'patients':searched_patients})

def UpdateRadiologist(request):
    profile = request.user.radiologistprofile
    radiologist_profile_form = RadiologistProfileForm(instance=profile)
    
    if request.method == 'POST':
        radiologist_profile_form = RadiologistProfileForm(request.POST, request.FILES, instance=profile)

        if radiologist_profile_form.is_valid():
            radiologist_profile_form.save()
            return redirect('radiologisthome')
    return render(request,'radiologist/radiologist_updateprofile.html', {'profile_form' : radiologist_profile_form})

@login_required(login_url='login')
def RadiologyOrders(request):
    radiologyorders = RadiologyOrder.objects.filter(status = False, payment = True)
    
    search_patient = request.GET.get('search')
    if search_patient:
        radiologyorders = RadiologyOrder.objects.filter(Q(Patient__first_name__icontains=search_patient) | Q(Patient__last_name__icontains=search_patient)
                                | Q(Patient__middle_name__icontains=search_patient) | Q(Patient__email__icontains=search_patient) | Q(Patient__phone__icontains=search_patient)).filter(status = False, payment = True)


    return render(request,'radiologist/radiologyorder.html', {'radiologyorders':radiologyorders})

def PatientProfile(request,pk):
    patient = Patient.objects.get(id=pk)
    radiologyorders = RadiologyOrder.objects.filter(Patient = patient, payment = True)
    return render(request,'radiologist/patientprofile.html', {'patient' : patient  , 'radiologyorders':radiologyorders})

def RadiologyResultForm(request,pk):
    radiologyorder = RadiologyOrder.objects.get(id = pk)
    radiologyresultform = ResultForm()

    if request.method == 'POST':
        form = ResultForm(request.POST, request.FILES)

        if form.is_valid():
            result = form.save(commit=False)
            result.order = radiologyorder
            result.technician = request.user.radiologistprofile
            radiologyorder.status = True
            radiologyorder.save()
            result.save()

            return redirect('radiologyresult', pk)
        
    return render(request,'radiologist/radiologyresultform.html', {'form' : radiologyresultform, 'radiologyorder':radiologyorder})

def RadiologyResults(request,pk):
    radiologyorder = RadiologyOrder.objects.get(id = pk)
    radiologyresults = RadiologyResult.objects.filter(order = radiologyorder)
    return render(request,'radiologist/radiologyresult.html', {'radiologyorder':radiologyorder, 'radiologyresults':radiologyresults})




@login_required(login_url='login')
def RadiologistMessages(request):
   
    chats = User.objects.all()

    array = []
    staffs = User.objects.all()
    for staff in staffs:
        chatcount = Messaging.objects.filter(sender=staff, receiver=request.user, seen = False)
        array.append(chatcount.count())
    
    zipped =zip(chats,array)

    context = {'chats':chats, 'array':array, 'zipped':zipped}
    
    return render(request,"radiologist/messages/messages_base.html", context)

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

    return render(request,"radiologist/messages/messages.html", context)


def file_view(request, pk):
    File = RadiologyResult.objects.get(id=pk).File
    with open('File', 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
    return response