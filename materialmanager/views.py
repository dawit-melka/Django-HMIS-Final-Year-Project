from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import MaterialManagerProfileForm, RegistrationForm, RegisterMaterialForm, InventoryRelocationForm,ServiceHistoryForm
from .models import Inventory,InventoryRelocation,ServiceHistory
from django.db.models import Q
from administrator.models import Messaging, Announcement
from django.contrib.auth.models import User
from django.contrib import messages

def RegisterMaterialManager(request):
    user_form = RegistrationForm()
    materialmanager_profile_form = MaterialManagerProfileForm()
    
    if request.method == 'POST':
        materialmanager_profile_form = MaterialManagerProfileForm(request.POST, request.FILES)
        user_form = RegistrationForm(request.POST, request.FILES)

        if user_form.is_valid():

            user = user_form.save()

            user.groups.add(8)

            materialmanager_profile = materialmanager_profile_form.save(commit=False)
            materialmanager_profile.material_manager = user
            materialmanager_profile.save()

            login(request,user)
            return redirect('after-login')
    return render(request,'materialmanager/register.html', {'user_form':user_form, 'profile_form' : materialmanager_profile_form , 'page': 'Material Manager' })


@login_required(login_url='login')
def MaterialManagerHome(request):
    announcements = Announcement.objects.all()[:2]
    return render(request,'materialmanager/materialmanager_home.html', {'announcements':announcements})

@login_required(login_url='login')
def Announcements(request):
    announcements = Announcement.objects.all()
    return render(request,'materialmanager/announcement.html',{'announcements':announcements})

@login_required(login_url='login')
def UpdateMaterialManager(request):
    profile = request.user.materialmanagerprofile
    materialmanager_profile_form = MaterialManagerProfileForm(instance=profile)
    
    if request.method == 'POST':
        materialmanager_profile_form = MaterialManagerProfileForm(request.POST, request.FILES, instance=profile)

        if materialmanager_profile_form.is_valid():
            materialmanager_profile_form.save()
            return redirect('materialmanagerhome')
    return render(request,'materialmanager/materialmanager_updateprofile.html', {'profile_form' : materialmanager_profile_form})


@login_required(login_url='login')
def SearchMaterial(request):
    search_material = request.GET.get('search')
    
    if search_material:
        searched_material = Inventory.objects.filter(Q(inventory_number__icontains=search_material) | Q(equipment_name__icontains=search_material)
                                | Q(equipment_type__icontains=search_material) | Q(model__icontains=search_material) | Q(serial_number__icontains=search_material) | Q(country_of_origin=search_material))
        
    else:
        searched_material = Inventory.objects.all()

    return render(request,'materialmanager/searchmaterial.html',{'materials':searched_material})

@login_required(login_url='login')
def RegisterMaterial(request):
    form = RegisterMaterialForm()

    if request.method == 'POST':
        form = RegisterMaterialForm(request.POST, request.FILES)

        if form.is_valid():
           
            register  = form.save(commit = False)
            register.registered_by = request.user.materialmanagerprofile
            register.save()

            return redirect('searchmaterial')

    return render(request,'materialmanager/registermaterial.html', {'form':form})


@login_required(login_url='login')
def Material(request,pk):
    material = Inventory.objects.get(inventory_number = pk)
    relocatematerials = InventoryRelocation.objects.filter(inventory=material)
    return render(request,'materialmanager/material.html', {'material':material , 'relocatematerials':relocatematerials})

@login_required(login_url='login')
def ServiceHistoryMaterial(request,pk):
    material = Inventory.objects.get(inventory_number = pk)
    servicehistorys = ServiceHistory.objects.filter(inventory=material)
    return render(request,'materialmanager/servicehistory.html', {'material':material, 'servicehistorys':servicehistorys})

@login_required(login_url='login')
def DisposeMaterial(request):

    search_material = request.GET.get('search')
    
    if search_material:
        searched_material = Inventory.objects.filter(Q(inventory_number__icontains=search_material) 
                                | Q(serial_number__icontains=search_material) )
        
    else:
        searched_material =None
    
    if request.method == 'POST' and request.POST.get('inventory_number'):
        inventory_number =request.POST.get('inventory_number')
        material  = Inventory.objects.get(inventory_number=inventory_number)
        print(material.inventory_number)
        material.dispose = True
        material.save()
    
    
        return redirect('material', inventory_number)
    return render(request,'materialmanager/disposematerial.html', {'materials':searched_material})

@login_required(login_url='login')
def RelocateMaterial(request):
    relocationform = InventoryRelocationForm()

    if request.method == 'POST':
        form = InventoryRelocationForm(request.POST)
        inventory_number = request.POST.get('inventory_number')
        print(inventory_number)

        try:
            inventory =Inventory.objects.get(inventory_number=inventory_number)
            print(inventory)
        except:
            messages.error(request, 'username doesnt exist')

        if form.is_valid() and inventory is not None:
            relocateform = form.save(commit=False)
            relocateform.inventory = inventory
            relocateform.save()
            
            return redirect('material', inventory_number)
    return render(request,'materialmanager/relocatematerial.html',{'forms':relocationform})

@login_required(login_url='login')
def FillServiceHistroy(request):
    serviceform = ServiceHistoryForm()

    if request.method == 'POST':
        form = ServiceHistoryForm(request.POST)
        inventory_number = request.POST.get('inventory_number')
        print(inventory_number)

        try:
            inventory =Inventory.objects.get(inventory_number=inventory_number)
            print(inventory)
        except:
            messages.error(request, 'username doesnt exist')
        
        if form.is_valid() and inventory is not None:
            servicehistory = form.save(commit=False)
            servicehistory.inventory = inventory
            servicehistory.material_manager = request.user.materialmanagerprofile

            servicehistory.save()
            
            return redirect('servicehistory', inventory_number)
            

    return render(request,'materialmanager/servicehistoryform.html',{'forms':serviceform})


@login_required(login_url='login')
def MaterialManagerMessages(request):
   

    chats = User.objects.all()

    array = []
    staffs = User.objects.all()
    for staff in staffs:
        chatcount = Messaging.objects.filter(sender=staff, receiver=request.user, seen = False)
        array.append(chatcount.count())
    
    zipped =zip(chats,array)

    context = {'chats':chats, 'array':array, 'zipped':zipped}
    
    return render(request,"materialmanager/messages/messages_base.html", context)

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
    
        return redirect('materialmanagermessagelist', pk=user.id)


    context = {'chats':chats, 'messageslist': messageslist, 'user':user, 'zipped':zipped}

    return render(request,"materialmanager/messages/messages.html", context)


def file_view(request, pk):
    File = Inventory.objects.get(id=pk).File
    with open('File', 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
    return response