from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from reception.models import ReceptionProfile
from cashier.models import CashierProfile
from nurse.models import NurseProfile
from doctor.models import DoctorProfile
from pharmacist.models import PharmacistProfile
from radiologist.models import RadiologistProfile
from labtechnician.models import LabTechnicianProfile
from materialmanager.models import MaterialManagerProfile


def RegisterDir(request):
    return render(request, 'registerdir.html')
######################## login logot ################################


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username)
        print(password)

        try:
            user =User.object.get(username=username)
        except:
            pass
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.groups.filter(name='Doctor').exists():
                return redirect('after-login')
            elif request.user.groups.filter(name='Reception').exists():
                return redirect('after-login')
            elif request.user.groups.filter(name='Pharmacist').exists():
                return redirect('after-login')
            elif request.user.groups.filter(name='Nurse').exists():
                return redirect('after-login')
            elif request.user.groups.filter(name='Cashier').exists():
                return redirect('after-login')
            elif request.user.groups.filter(name='Lab').exists():
                return redirect('after-login')
            elif request.user.groups.filter(name='Radiologist').exists():
                return redirect('after-login')
            elif request.user.groups.filter(name='Materialmanager').exists():
                return redirect('after-login')
            elif request.user.groups.filter(name='Administrator').exists():
                return redirect('adminhome')
        else:
            messages.error(request, 'Incorrect password or Username')

    return render(request,'login.html')

def afterLogin(request):
    
    if request.user.groups.filter(name='Reception').exists():
        account_approval = ReceptionProfile.objects.get(recepetion=request.user).active
        if account_approval:
            return redirect('receptionhome')
        else:
            return render(request, 'pending_approval.html')
        
    if request.user.groups.filter(name='Cashier').exists():
        account_approval = CashierProfile.objects.get(cashier=request.user).active
        if account_approval:
            return redirect('cashierhome')
        else:
            return render(request, 'pending_approval.html') 
        
    if request.user.groups.filter(name='Nurse').exists():
        account_approval = NurseProfile.objects.get(nurse=request.user).active
        if account_approval:
            return redirect('nursehome')
        else:
            return render(request, 'pending_approval.html') 
        
    if request.user.groups.filter(name='Doctor').exists():
        account_approval = DoctorProfile.objects.get(doctor=request.user).active
        if account_approval:
            return redirect('doctorhome')
        else:
            return render(request, 'pending_approval.html')  
        
    if request.user.groups.filter(name='Lab').exists():
        account_approval = LabTechnicianProfile.objects.get(labtechnician=request.user).active
        if account_approval:
            return redirect('labtechnicianhome')
        else:
            return render(request, 'pending_approval.html') 
        
    if request.user.groups.filter(name='Radiologist').exists():
        account_approval = RadiologistProfile.objects.get(radiologist=request.user).active
        if account_approval:
            return redirect('radiologisthome')
        else:
            return render(request, 'pending_approval.html') 
    
    if request.user.groups.filter(name='Materialmanager').exists():
        account_approval = MaterialManagerProfile.objects.get(material_manager=request.user).active
        if account_approval:
            return redirect('materialmanagerhome')
        else:
            return render(request, 'pending_approval.html') 
   
    if request.user.groups.filter(name='Pharmacist').exists():
        account_approval = PharmacistProfile.objects.get(pharmacist=request.user).active
        if account_approval:
            return redirect('pharmacisthome')
        else:
            return render(request, 'pending_approval.html') 

@login_required()
def LogoutPage(request):
    logout(request)
    return redirect('login')