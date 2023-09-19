from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import AdminProfileForm, AnnouncementForm
from django.contrib.auth.models import User
from .models import Announcement
from doctor.models import DoctorProfile,LabOrder, RadiologyOrder, PrescribedMedicine
from reception.models import ReceptionProfile,Patient, Appointment
from cashier.models import CashierProfile
from nurse.models import NurseProfile
from radiologist.models import RadiologistProfile
from pharmacist.models import PharmacistProfile
from labtechnician.models import LabTechnicianProfile
from materialmanager.models import MaterialManagerProfile
from . forms import ExcelForm
from datetime import datetime, date
from operator import attrgetter

from administrator.models import Messaging
import xlwt

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageTemplate, Frame, NextPageTemplate, PageBreak, Image
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

import base64
import matplotlib.pyplot as plt
from PIL import Image as PILImage

import collections
from django.contrib import messages



@login_required(login_url='login')
def AdminHome(request):
    announcements = Announcement.objects.all().order_by('-created')[:2]
    pending_approvals = 0
    pending_approvals += ReceptionProfile.objects.filter(active=False).count()
    pending_approvals += DoctorProfile.objects.filter(active=False).count()
    pending_approvals += NurseProfile.objects.filter(active=False).count()
    pending_approvals += RadiologistProfile.objects.filter(active=False).count()
    pending_approvals += LabTechnicianProfile.objects.filter(active=False).count()
    pending_approvals += PharmacistProfile.objects.filter(active=False).count()
    pending_approvals += MaterialManagerProfile.objects.filter(active=False).count()
    pending_approvals += CashierProfile.objects.filter(active=False).count()
    context = {'announcements':announcements,
               'pending_approvals': pending_approvals}
    return render(request,'administrator/admin_home.html', context)

@login_required(login_url='login')
def UpdateAdmin(request):
    profile = request.user.adminprofile
    admin_profile_form = AdminProfileForm(instance=profile)
    
    if request.method == 'POST':
        admin_profile_form = AdminProfileForm(request.POST, request.FILES, instance=profile)

        if admin_profile_form.is_valid():
            admin_profile_form.save()
            return redirect('adminhome')
    return render(request,'administrator/admin_updateprofile.html', {'profile_form' : admin_profile_form})

@login_required(login_url='login')
def ApproveRequests(request):
    users = User.objects.all()
    if request.method == 'POST' and request.POST.get('delete'):
        user_id =request.POST.get('delete')
        user = User.objects.get(id=user_id)
        user.delete()
    return render(request,'administrator/approverequests.html', {'users':users})

@login_required(login_url='login')
def SearchStaff(request):
    users = User.objects.all()
    return render(request,'administrator/searchstaff.html', {'users':users})


@login_required(login_url='login')
def Announcements(request):
    announcements = Announcement.objects.all().order_by('-created')
    if request.method == 'POST' and request.POST.get('delete'):
        announcement_id =request.POST.get('delete')
        announcement = Announcement.objects.get(id=announcement_id)
        announcement.delete()
    return render(request,'administrator/announcement.html',{'announcements':announcements})

@login_required(login_url='login')
def CreateAnnouncements(request):
    profile = request.user.adminprofile
    announcement_form = AnnouncementForm()
    
    if request.method == 'POST':
        announcement_form = AnnouncementForm(request.POST, request.FILES)

        if announcement_form.is_valid():
            an = announcement_form.save(commit=False)
            an.administrator = profile
            an.save()
            return redirect('announcements')
    return render(request,'administrator/createannouncement.html',{'form':announcement_form})

@login_required(login_url='login')
def Report(request):
    patients = Patient.objects.all()
    form = ExcelForm()

    specified_year = 2023
    registeration_dates = [patient.created for patient in patients if patient.created.year == specified_year]
    monthly_counts = collections.Counter(date.month for date in registeration_dates)
    months = list(range(1, 13))
    counts = [monthly_counts[month] for month in months]


    # Create the bar chart
    blood_types = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    blood_type_counts = {blood_type: 0 for blood_type in blood_types}

    # create pie chart
    genders = 'Female', 'Male'

    female = 0
    male = 0 
    
    for p in patients:
        if p.gender == 'Female':
            female += 1
        if p.gender == 'Male':
            male += 1

    gender_type_counts = [female,male]

    

    for patient in patients:
        blood_type_counts[patient.get_bloodtype] += 1  # Replace 'bloodtype' with the correct field name
    
    # Create the bar chart for blood types
    fig, axis = plt.subplots(nrows=2, ncols=2, figsize=(10, 12))
    axis[0, 0].bar(blood_types, blood_type_counts.values())
    axis[0, 0].set_xlabel('Blood Type')
    axis[0, 0].set_ylabel('Number of Patients')
    axis[0, 0].set_title('Patients by Blood Type')

    # Create the histogram for age distribution
    num_bins = 10
    age_range = (0, 100)
    ages = [patient.get_age for patient in patients]  # Replace 'age' with the correct field name
    axis[0, 1].hist(ages, bins=num_bins, range=age_range, edgecolor='white', color='#005b96')
    axis[0, 1].set_xlabel('Age')
    axis[0, 1].set_ylabel('Number of Patients')
    axis[0, 1].set_title('Patients by Age')

    #
    axis[1,0].pie(gender_type_counts , labels = genders)
    axis[1, 0].set_title('Patients by Gender')
    #
    axis[1, 1].plot(months, counts, marker='o', color='blue')
    axis[1, 1].set_xticks(months)
    axis[1, 1].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axis[1, 1].set_xlabel('Month')
    axis[1, 1].set_ylabel('Number of Patients')
    axis[1, 1].set_title(f'Patients Admitted in {specified_year}')

    # Adjust the spacing between the subplots
    plt.subplots_adjust(hspace=1)

    # Save the combined charts as an image in memory
    chart_buffer = io.BytesIO()
    plt.savefig(chart_buffer, format='png')
    chart_buffer.seek(0)

    # Encode the image as a base64 string
    chart_base64 = base64.b64encode(chart_buffer.getvalue()).decode('utf-8')

    context = {
        'chart_base64': chart_base64,
        'patients': patients,
        'form': form
    }
    return render(request,'administrator/reports.html',context)


#############################################################################################################
def ApproveReception(request, pk):
    reception = ReceptionProfile.objects.get(id=pk)
    user = reception.recepetion
    email = reception.recepetion.email
    if request.method == 'POST'and request.POST.get('approve'):
        reception.active = True
        reception.save()
        return redirect('approverequests')  
    
    if request.method == 'POST'and request.POST.get('delete'):
        user.delete()
        return redirect('approverequests') 

    context = { 'user': reception, 'role': 'Reception', 'email':email}
    return render(request, "administrator/approving.html", context)

def ApproveCashier(request, pk):
    cashier = CashierProfile.objects.get(id=pk)
    user = cashier.cashier
    email = cashier.cashier.email
    if request.method == 'POST'and request.POST.get('approve'):
        cashier.active = True
        cashier.save()
        return redirect('approverequests')  
    
    if request.method == 'POST'and request.POST.get('delete'):
        user.delete()
        return redirect('approverequests') 

    context = { 'user': cashier, 'role': 'Cashier', 'email':email}
    return render(request, "administrator/approving.html", context)
def ApproveNurse(request, pk):
    nurse = NurseProfile.objects.get(id=pk)
    user = nurse.nurse
    email = nurse.nurse.email
    if request.method == 'POST'and request.POST.get('approve'):
        nurse.active = True
        nurse.save()
        return redirect('approverequests')  
    
    if request.method == 'POST'and request.POST.get('delete'):
        user.delete()
        return redirect('approverequests') 

    context = { 'user': nurse, 'role': 'Nurse', 'email':email}
    return render(request, "administrator/approving.html", context)

def ApproveDoctor(request, pk):
    doctor = DoctorProfile.objects.get(id=pk)
    user = doctor.doctor
    email = doctor.doctor.email
    if request.method == 'POST'and request.POST.get('approve'):
        doctor.active = True
        doctor.save()
        return redirect('approverequests')  
    
    if request.method == 'POST'and request.POST.get('delete'):
        user.delete()
        return redirect('approverequests') 

    context = { 'user': doctor, 'role': 'Doctor', 'email':email}
    return render(request, "administrator/approving.html", context)

def ApprovePharmacist(request, pk):
    pharmacist = PharmacistProfile.objects.get(id=pk)
    user = pharmacist.pharmacist
    email = pharmacist.pharmacist.email
    if request.method == 'POST'and request.POST.get('approve'):
        pharmacist.active = True
        pharmacist.save()
        return redirect('approverequests')  
    
    if request.method == 'POST'and request.POST.get('delete'):
        user.delete()
        return redirect('approverequests') 

    context = { 'user': pharmacist, 'role': 'Pharmacist', 'email':email}
    return render(request, "administrator/approving.html", context)

def ApproveRadiologist(request, pk):
    radiologist = RadiologistProfile.objects.get(id=pk)
    user = radiologist.radiologist
    email = radiologist.radiologist.email
    if request.method == 'POST'and request.POST.get('approve'):
        radiologist.active = True
        radiologist.save()
        return redirect('approverequests')  
    
    if request.method == 'POST'and request.POST.get('delete'):
        user.delete()
        return redirect('approverequests') 

    context = { 'user': radiologist, 'role': 'Radiologist', 'email':email}
    return render(request, "administrator/approving.html", context)
def ApproveLab(request, pk):
    lab = LabTechnicianProfile.objects.get(id=pk)
    user = lab.labtechnician
    email = lab.labtechnician.email
    if request.method == 'POST'and request.POST.get('approve'):
        lab.active = True
        lab.save()
        return redirect('approverequests')  
    
    if request.method == 'POST'and request.POST.get('delete'):
        user.delete()
        return redirect('approverequests') 

    context = { 'user': lab, 'role': 'Lab Technician', 'email':email}
    return render(request, "administrator/approving.html", context)
def ApproveMaterial(request, pk):
    material = MaterialManagerProfile.objects.get(id=pk)
    user = material.material_manager
    email = material.material_manager.email
    if request.method == 'POST'and request.POST.get('approve'):
        material.active = True
        material.save()
        return redirect('approverequests')  
    
    if request.method == 'POST'and request.POST.get('delete'):
        user.delete()
        return redirect('approverequests') 

    context = { 'user': material, 'role': 'Material Manager', 'email':email}
    return render(request, "administrator/approving.html", context)
##############################################################################################
def DeleteReception(request, pk):
    reception = ReceptionProfile.objects.get(id=pk)
    user = reception.recepetion
    email = reception.recepetion.email  
    
    if request.method == 'POST'and request.POST.get('delete'):
        user.delete()
        return redirect('approverequests') 

    context = { 'user': reception, 'role': 'Reception', 'email':email}
    return render(request, "administrator/deletestaff.html", context)

def DeleteCashier(request, pk):
    cashier = CashierProfile.objects.get(id=pk)
    user = cashier.cashier
    email = cashier.cashier.email
    
    if request.method == 'POST'and request.POST.get('delete'):
        user.delete()
        return redirect('approverequests') 

    context = { 'user': cashier, 'role': 'Cashier', 'email':email}
    return render(request, "administrator/deletestaff.html", context)

def DeleteNurse(request, pk):
    nurse = NurseProfile.objects.get(id=pk)
    user = nurse.nurse
    email = nurse.nurse.email
    
    if request.method == 'POST'and request.POST.get('delete'):
        user.delete()
        return redirect('approverequests') 

    context = { 'user': nurse, 'role': 'Nurse', 'email':email}
    return render(request, "administrator/deletestaff.html", context)

def DeleteDoctor(request, pk):
    doctor = DoctorProfile.objects.get(id=pk)
    user = doctor.doctor
    email = doctor.doctor.email  
    
    if request.method == 'POST'and request.POST.get('delete'):
        user.delete()
        return redirect('approverequests') 

    context = { 'user': doctor, 'role': 'Doctor', 'email':email}
    return render(request, "administrator/deletestaff.html", context)

def DeletePharmacist(request, pk):
    pharmacist = PharmacistProfile.objects.get(id=pk)
    user = pharmacist.pharmacist
    email = pharmacist.pharmacist.email 
    
    if request.method == 'POST'and request.POST.get('delete'):
        user.delete()
        return redirect('approverequests') 

    context = { 'user': pharmacist, 'role': 'Pharmacist', 'email':email}
    return render(request, "administrator/deletestaff.html", context)

def DeleteRadiologist(request, pk):
    radiologist = RadiologistProfile.objects.get(id=pk)
    user = radiologist.radiologist
    email = radiologist.radiologist.email
    
    if request.method == 'POST'and request.POST.get('delete'):
        user.delete()
        return redirect('approverequests') 

    context = { 'user': radiologist, 'role': 'Radiologist', 'email':email}
    return render(request, "administrator/deletestaff.html", context)

def DeleteLab(request, pk):
    lab = LabTechnicianProfile.objects.get(id=pk)
    user = lab.labtechnician
    email = lab.labtechnician.email 
    
    if request.method == 'POST'and request.POST.get('delete'):
        user.delete()
        return redirect('approverequests') 

    context = { 'user': lab, 'role': 'Lab Technician', 'email':email}
    return render(request, "administrator/deletestaff.html", context)

def DeleteMaterial(request, pk):
    material = MaterialManagerProfile.objects.get(id=pk)
    user = material.material_manager
    email = material.material_manager.email  
    
    if request.method == 'POST'and request.POST.get('delete'):
        user.delete()
        return redirect('approverequests') 

    context = { 'user': material, 'role': 'Material Manager', 'email':email}
    return render(request, "administrator/deletestaff.html", context)
##########################################################################################

@login_required(login_url='login')
def AdminMessages(request):
   

    chats = User.objects.all()

    array = []
    staffs = User.objects.all()
    for staff in staffs:
        chatcount = Messaging.objects.filter(sender=staff, receiver=request.user, seen = False)
        array.append(chatcount.count())
    
    zipped =zip(chats,array)

    context = {'chats':chats, 'array':array, 'zipped':zipped}
    
    return render(request,"administrator/messages/messages_base.html", context)

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
    
        return redirect('receptionmessagelist', pk=user.id)


    context = {'chats':chats, 'messageslist': messageslist, 'user':user, 'zipped':zipped}

    return render(request,"administrator/messages/messages.html", context)
###################################################################################3333


@login_required(login_url='login')
def PatientsReport(request):
    patients = Patient.objects.all()

    specified_year = 2023
    registeration_dates = [patient.created for patient in patients if patient.created.year == specified_year]
    monthly_counts = collections.Counter(date.month for date in registeration_dates)
    months = list(range(1, 13))
    counts = [monthly_counts[month] for month in months]


    # Create the bar chart
    blood_types = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    blood_type_counts = {blood_type: 0 for blood_type in blood_types}

    # create pie chart
    genders = 'Female', 'Male'

    female = 0
    male = 0 
    
    for p in patients:
        if p.gender == 'Female':
            female += 1
        if p.gender == 'Male':
            male += 1

    gender_type_counts = [female,male]

    

    for patient in patients:
        blood_type_counts[patient.get_bloodtype] += 1  # Replace 'bloodtype' with the correct field name
    
    # Create the bar chart for blood types
    fig, axis = plt.subplots(nrows=3, ncols=2, figsize=(10, 14))
    axis[1, 0].bar(blood_types, blood_type_counts.values())
    axis[1, 0].set_xlabel('Blood Type')
    axis[1, 0].set_ylabel('Number of Patients')
    axis[1, 0].set_title('Patients by Blood Type')

    # Create the histogram for age distribution
    num_bins = 10
    age_range = (0, 100)
    ages = [patient.get_age for patient in patients]  # Replace 'age' with the correct field name
    axis[1, 1].hist(ages, bins=num_bins, range=age_range, edgecolor='white', color='#005b96')
    axis[1, 1].set_xlabel('Age')
    axis[1, 1].set_ylabel('Number of Patients')
    axis[1, 1].set_title('Patients by Age')

    # Create Pie char for age groups
    pediatric_count = len([age for age in ages if age < 18])
    youth_count = len([age for age in ages if 18 <= age < 35])
    middle_age_count = len([age for age in ages if 35 <= age < 65])
    elderly_count = len([age for age in ages if age >= 65])

    age_groups = ['Pediatric', 'Youth', 'Middle Age', 'Elderly']
    age_group_counts = [pediatric_count, youth_count, middle_age_count, elderly_count]

    axis[0, 0].remove()
    axis[0, 1].remove()
    merged_axis = fig.add_subplot(2, 3, 2)
    wedges, texts, autotexts = merged_axis.pie(age_group_counts, autopct='%1.1f%%', startangle=90)
    merged_axis.set_title('Patients by Age Group')
    merged_axis.legend(wedges, age_groups, title="Age Group", loc="center left", bbox_to_anchor=(1, 0.1, 0.6, 1.4), fontsize=12)
    #
    axis[2,0].pie(gender_type_counts , labels = genders, startangle=90)
    axis[2, 0].set_title('Patients by Gender')
    # axis[2,0].legend(wedges, genders, title="Gender", loc="center left", bbox_to_anchor=(0.8, 0.2, 0.6, 1.4), fontsize=12)
    #
    axis[2, 1].plot(months, counts, marker='o', color='blue')
    axis[2, 1].set_xticks(months)
    axis[2, 1].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axis[2, 1].set_xlabel('Month')
    axis[2, 1].set_ylabel('Number of Patients')
    axis[2, 1].set_title(f'Patients Admitted in {specified_year}')

    # Adjust the spacing between the subplots
    plt.subplots_adjust(hspace=0.8)

    # Save the combined charts as an image in memory
    chart_buffer = io.BytesIO()
    plt.savefig(chart_buffer, format='png')
    chart_buffer.seek(0)

    # Encode the image as a base64 string
    chart_base64 = base64.b64encode(chart_buffer.getvalue()).decode('utf-8')

    context = {
        'chart': chart_base64,
        'patients': patients,
    }
    return render(request,'administrator/patientsreport.html',context)

def StaffsReport(request):
    role_counts = [
        ReceptionProfile.objects.filter(active=True).count(),
        DoctorProfile.objects.filter(active=True).count(),
        NurseProfile.objects.filter(active=True).count(),
        LabTechnicianProfile.objects.filter(active=True).count(),
        RadiologistProfile.objects.filter(active=True).count(),
        PharmacistProfile.objects.filter(active=True).count(),
        MaterialManagerProfile.objects.filter(active=True).count(),
        CashierProfile.objects.filter(active=True).count()
    ]
    roles = [
        'Receptionist', 'Doctor', 'Nurse',
        'Lab Technician', 'Radiologist', 
        'Pharmacist', 'Biomedical Engineer', 
        'Cashiers'
    ]

    specialization_counts = {}
    for doctor in DoctorProfile.objects.filter(active=True):
        if doctor.Specalization.specalization not in specialization_counts:
            specialization_counts[doctor.Specalization.specalization] = 1
        else:
            specialization_counts[doctor.Specalization.specalization] += 1
    
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 10))
    print(specialization_counts)

    # Staff Distribution by Role Pie Chart
    colors = ['#8ecae6', '#d62828', '#3CAEA3', '#F6D55C', '#ED553B', '#20639B', '#FFB6C1', '#FF69B4']
    wedges, texts, autotexts = ax1.pie(role_counts, startangle=90, colors=colors, autopct=lambda pct: str(round(pct,2)) + '%\n(' + str(int(pct / 100.0 * sum(role_counts))) + ')')
    ax1.axis('equal')
    ax1.set_title('Staff Distribution by Role', fontdict={'fontsize': 14})

    # Place the legend to the right of the pie chart
    ax1.legend(wedges, roles, title="Roles", loc="center left", bbox_to_anchor=(0.8, 0.2, 0.6, 1.4), fontsize=12)

    # Doctor Distribution by Specialization Bar Chart
    colors = ['#FF7F50', '#FF6347', '#FF4500', '#FF8C00', '#FFB6C1', '#FF69B4', '#FF1493', '#9400D3']
    
    ax2.bar(specialization_counts.keys(), specialization_counts.values(), color=colors[:len(specialization_counts)])
    ax2.set_title('Doctor Distribution by Specialization', fontdict={'fontsize': 14})
    ax2.set_xlabel('Specialization', fontsize=12)
    ax2.set_ylabel('Number of Doctors', fontsize=12)
    # ax2.tick_params(axis='x', labelrotation=45)

    chart_buffer = io.BytesIO()
    plt.savefig(chart_buffer, format='png')
    
    chart_buffer.seek(0)

    chart_base64 = base64.b64encode(chart_buffer.getvalue()).decode('utf-8')
    context = {'chart': chart_base64}

    return render(request, 'administrator/staffsreport.html', context)


def FinancialReport(request):
    appointments_total = sum([appointment.total_price for appointment in Appointment.objects.filter(payment=True)])
    laborder_total = sum([laborder.total_price for laborder in LabOrder.objects.filter(payment=True)])
    radiologyorder_total = sum([radiologyorder.total_price for radiologyorder in RadiologyOrder.objects.filter(payment=True)])

    payment_totals = [appointments_total, laborder_total, radiologyorder_total]

    fig, ax = plt.subplots(figsize=(10, 6))
    roles = ['Appointments', 'Lab Orders', 'Radiology Orders']

    wedges, texts, autotexts = ax.pie(payment_totals, autopct=lambda pct: "{:.1f}%\n({:.2f})".format(pct, pct/100*sum(payment_totals)), startangle=90)
    ax.set_title('Payments by Type', fontsize=16)
    ax.legend(wedges, roles, title="Roles", loc="center left", bbox_to_anchor=(0.8, 0.2, 0.6, 1.4), fontsize=12)

    chart_buffer = io.BytesIO()
    plt.savefig(chart_buffer, format='png')
    chart_buffer.seek(0)

    chart_base64 = base64.b64encode(chart_buffer.getvalue()).decode('utf-8')
    context = {'chart': chart_base64}

    return render(request, 'administrator/financialreport.html', context)



def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-disposition'] = 'attachment; filename=Patients_List'+ \
        str(datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Patient List')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Patient id','Patient Name','Type', 'Doctor(appointment doctor /orderd by)', 'Creation Date','Cashier', 'Price']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()
    
    appointments = Appointment.objects.filter(payment = True)
    laborder = LabOrder.objects.filter(payment = True)
    radiologyorder = RadiologyOrder.objects.filter(payment = True)


    payments = sorted(
        [*appointments, *laborder, *radiologyorder],
        key=attrgetter('payment_date'),
        reverse=True
    )

    for payment in payments:
        try:
            if payment.radio:
                type = 'Radiology'
        except:
            try:
                if payment.lab:
                    type = 'Lab'
            except:
                type = 'Appointment'

        row_num += 1
        ws.write(row_num, 0, str(payment.Patient.id))
        ws.write(row_num, 1, str(payment.Patient.first_name))
        ws.write(row_num, 2, str(type))
        ws.write(row_num, 3, str(payment.Doctor))
        ws.write(row_num, 4, str(payment.created))
        ws.write(row_num, 5, str(payment.Cashier))
        ws.write(row_num, 6, str(payment.total_price))

    wb.save(response)
    return response