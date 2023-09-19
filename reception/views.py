from django.shortcuts import render, redirect, HttpResponse
from .models import ReceptionProfile, Appointment,Patient
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm,PatientRegistrationForm, BookAppointmentForm, ReceptionProfileForm, BookAppointmentfromProfileForm
from django.contrib.auth import authenticate, login ,logout
from doctor.models import DoctorProfile
from django.db.models import Q
from datetime import datetime, date
from django.contrib.auth.models import User
from administrator.models import Messaging, Announcement
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

plt.style.use('ggplot')

def RegisterReception(request):
    user_form = RegistrationForm()
    reception_profile_form = ReceptionProfileForm()
    
    if request.method == 'POST':
        reception_profile_form = ReceptionProfileForm(request.POST, request.FILES)
        user_form = RegistrationForm(request.POST)

        if user_form.is_valid():

            user = user_form.save()

            user.groups.add(1)

            reception_profile = reception_profile_form.save(commit=False)
            reception_profile.recepetion = user
            reception_profile.save()

            login(request,user)
            return redirect('after-login')
    return render(request,'reception/register.html', {'user_form':user_form, 'profile_form' : reception_profile_form , 'page': 'Reception' })

@login_required(login_url='login')
def ReceptionBase(request):
    chatcount = Messaging.objects.filter(receiver=request.user, seen = False).count()
    return render(request,'reception/rec_base.html',{'chatcount':chatcount})

@login_required(login_url='login')
def ReceptionHome(request):
    doctors_working_now = DoctorProfile.objects.filter(is_working_now=True).count()
    announcements = Announcement.objects.all()[:2]
    return render(request,'reception/reception_home.html',{'announcements':announcements, 'doctors_working_now' : doctors_working_now})

def UpdateReception(request):
    profile = request.user.receptionprofile
    reception_profile_form = ReceptionProfileForm(instance=profile)
    
    if request.method == 'POST':
        reception_profile_form = ReceptionProfileForm(request.POST, request.FILES, instance=profile)

        if reception_profile_form.is_valid():
            reception_profile_form.save()
            return redirect('receptionhome')
    return render(request,'reception/reception_updateprofile.html', {'profile_form' : reception_profile_form})

@login_required(login_url='login')
def Announcements(request):
    announcements = Announcement.objects.all()
    return render(request,'reception/announcement.html',{'announcements':announcements})

@login_required(login_url='login')
def Report(request):
    patients = Patient.objects.all()

    context = {
        'patients': patients,
    }
    return render(request,'reception/reports.html',context)

@login_required(login_url='login')
def RegisterPatient(request):
    form = PatientRegistrationForm()

    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            patient_form = form.save(commit=False)
            patient_form.reception = request.user
            patient_form.save()

            return redirect('searchpatients')

    return render(request,'reception/register_patient.html', {'form':form})

@login_required(login_url='login')
def EditPatient(request,pk):

    patient = Patient.objects.get(id=pk)
    form = PatientRegistrationForm(instance=patient)

    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST, request.FILES,instance=patient)

        if form.is_valid():
            patient_form = form.save(commit=False)
            patient_form.reception = request.user
            patient_form.save()

            return redirect('patientprofile', pk)

    return render(request,'reception/editpatient.html', {'form':form})



@login_required(login_url='login')
def SearchPatients(request):
    search_patient = request.GET.get('search')
    
    if search_patient:
        searched_patients = Patient.objects.filter(Q(first_name__icontains=search_patient) | Q(last_name__icontains=search_patient)
                                | Q(middle_name__icontains=search_patient) | Q(email__icontains=search_patient) | Q(phone__icontains=search_patient))
    else:
        searched_patients=Patient.objects.all()

    return render(request,'reception/searchpatients.html',{'patients':searched_patients})


@login_required(login_url='login')
def BookAppointment(request):
    form = BookAppointmentForm()

    if request.method == 'POST':
        form = BookAppointmentForm(request.POST)
        patientid = request.POST.get('patientid')
        date = request.POST['date']
        time = request.POST['time']

        try:
            patient =Patient.objects.get(id=patientid)

            if form.is_valid() and patient is not None:
                
                appform = form.save(commit=False)
                appform.Patient = patient
                appform.save()
                
                if patient.email:
                    subject = 'Hospital Appointment'
                    message = f'Hi {patient.first_name} {patient.middle_name} {patient.last_name}, Your hospital appointment will be on {time} {date}. Kind regards'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [patient.email, ]
                    send_mail( subject, message, email_from, recipient_list )
                return redirect('patientprofile', patientid)          
        except:
            messages.warning(request, 'Patient Doesnt Exist')

    return render(request,'reception/book_appointment.html', {'form':form})


from django.conf import settings
from django.core.mail import send_mail

@login_required(login_url='login')
def BookAppointmentfromProfile(request,pk):
    patient = Patient.objects.get(id=pk)
    form = BookAppointmentfromProfileForm()

    if request.method == 'POST':
        form = BookAppointmentfromProfileForm(request.POST)
        date = request.POST['date']
        time = request.POST['time']

        if form.is_valid():
            bookappointment = form.save(commit=False)
            bookappointment.Patient= patient
            bookappointment.save()

            if patient.email:
                subject = 'Hospital Appointment'
                message = f'Hi {patient.first_name} {patient.middle_name} {patient.last_name}, Your hospital appointment will be on {time} {date}. Kind regards'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [patient.email, ]
                send_mail( subject, message, email_from, recipient_list )

            return redirect('patientprofile', patient.id)


    return render(request,'reception/book_appointment_profile.html', {'form':form})

@login_required(login_url='login')
def RescheduleAppointment(request, pk):
    appointment = Appointment.objects.get(id=pk)
    form = BookAppointmentfromProfileForm(instance=appointment)

    if request.method == 'POST':
        form = BookAppointmentfromProfileForm(request.POST, instance=appointment)

        if form.is_valid():
            form.save()
            return redirect('appointments')
        

    return render(request,'reception/book_appointment_profile.html', {'form':form})

@login_required(login_url='login')
def Appointments(request):
    today = datetime.today().date()
    appointments = Appointment.objects.filter(date=today)
    
    search_patient = request.GET.get('search')
    if search_patient:
        appointments = Appointment.objects.filter(Q(Patient__first_name__icontains=search_patient) | Q(Patient__last_name__icontains=search_patient)
                                | Q(Patient__middle_name__icontains=search_patient) | Q(Patient__email__icontains=search_patient) | Q(Patient__phone__icontains=search_patient))

    if request.method == 'POST' and request.POST.get('today')=='today':
        appointments = Appointment.objects.filter(date=today)

    if request.method == 'POST' and request.POST.get('alltime')=='alltime':
        appointments = Appointment.objects.all()

    if request.method == 'POST' and request.POST.get('appointment_id'):
        appointment_id =request.POST.get('appointment_id')
        appointment  = Appointment.objects.get(id=appointment_id)
        if appointment.status == False:
            appointment.status=True
            appointment.save()
        else:
            appointment.status = False
            appointment.save()
    
    if request.method == 'POST' and request.POST.get('delete'):
        appointment_id = request.POST.get('delete')
        appointment  = Appointment.objects.get(id=appointment_id)
        appointment.delete()

    filter_active = 'alltime' if request.POST.get('alltime') == 'alltime' else 'today'
    return render(request,'reception/appointments.html', {'appointments':appointments, 'filter_active': filter_active})


def load_Doctors(request):
    Specalization_id = request.GET.get('Specalization')
    Doctors = DoctorProfile.objects.filter(Specalization_id=Specalization_id).order_by('first_name')
    return render(request, 'reception/doctor_dropdown.html', {'Doctors': Doctors})

def UpdatePatient(request,pk):
    patient=Patient.objects.get(id=pk)
    form = PatientRegistrationForm(instance=patient)

    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST, request.FILES, instance=patient)

        if form.is_valid():
            form.save()


            return redirect('receptionhome')
    return render(request,'reception/updatepatient.html', {'form':form})

def load_Doctors(request):
    Specalization_id = request.GET.get('Specalization')
    Doctors = DoctorProfile.objects.filter(Specalization_id=Specalization_id).order_by('first_name')
    return render(request, 'reception/doctor_dropdown.html', {'Doctors': Doctors})

@login_required(login_url='login')
def PatientProfile(request,pk):

    patient = Patient.objects.get(id=pk)
    appointments = Appointment.objects.filter(Patient = patient)

    if request.method == 'POST' and request.POST.get('appointment_id'):
        appointment_id =request.POST.get('appointment_id')
        appointment  = Appointment.objects.get(id=appointment_id)
        if appointment.status == False:
            appointment.status=True
            appointment.save()
        else:
            appointment.status = False
            appointment.save()
    
    if request.method == 'POST' and request.POST.get('delete'):
        appointment_id = request.POST.get('delete')
        appointment  = Appointment.objects.get(id=appointment_id)
        appointment.delete()
    
    return render(request,"reception/patientprofile.html",{'patient':patient, 'appointments':appointments })

@login_required(login_url='login')
def ReceptionMessages(request):
   

    chats = User.objects.all()

    array = []
    staffs = User.objects.all()
    for staff in staffs:
        chatcount = Messaging.objects.filter(sender=staff, receiver=request.user, seen = False)
        array.append(chatcount.count())
    
    zipped =zip(chats,array)

    context = {'chats':chats, 'array':array, 'zipped':zipped}
    
    return render(request,"reception/messages/messages_base.html", context)

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

    return render(request,"reception/messages/messages.html", context)

def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-disposition'] = 'attachment; filename=Patients_List'+ \
        str(datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Patient List')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Name','Gender', 'Age','Marital Status', 'Blood Type', 'Phone','Email','Address','Emergency Contact Name', 'Relationship', 'Emergncy Contact Phone']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()
    patients = Patient.objects.all()

    for patient in patients:
        row_num += 1
        ws.write(row_num, 0, str(patient.get_name))
        ws.write(row_num, 1, str(patient.gender))
        ws.write(row_num, 2, str(patient.get_age))
        ws.write(row_num, 3, str(patient.marital_status))
        ws.write(row_num, 4, str(patient.get_bloodtype))
        ws.write(row_num, 5, str(patient.phone))
        ws.write(row_num, 6, str(patient.email))
        ws.write(row_num, 7, str(patient.get_address))
        ws.write(row_num, 8, str(patient.emergency_contact_name))
        ws.write(row_num, 9, str(patient.relationship))
        ws.write(row_num, 10, str(patient.contact_phone))

    wb.save(response)
    return response

def draw_page(canvas, doc):
    # Draw the title
    canvas.setFont('Helvetica-Bold', 20)
    canvas.drawCentredString(letter[0] / 2, letter[1] - inch, 'Patients List')

    # Draw the page number
    canvas.setFont('Helvetica', 10)
    page_number = f"Page {doc.page}"
    canvas.drawRightString(letter[0] - inch, inch / 2, page_number)


def export_pdf(request):
    patients = Patient.objects.all()

    # Define the table data
    data = [['Name','Gender', 'Age','Marital Status', 'Blood Type', 'Phone']]
    for patient in patients:
        data.append([patient.get_name,patient.gender, patient.get_age, patient.marital_status, patient.get_bloodtype, patient.phone])

    # Create the PDF document
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Define the main content frame
    main_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='main_frame')

    # Create a custom PageTemplate with the main content frame and the draw_page event handler function
    main_page_template = PageTemplate(id='main_page_template', frames=main_frame, onPage=draw_page)
    doc.addPageTemplates([main_page_template])

    # Define the table style
    table_style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background color
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
    ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header bottom padding
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Table row background color
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Table row text color
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Table row font
    ('FONTSIZE', (0, 1), (-1, -1), 10),  # Table row font size
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Table alignment
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Table vertical alignment
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Table grid
    ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Inner grid color and thickness
    ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Outer border color and thickness
    ('LEFTPADDING', (0, 0), (-1, -1), 10),  # Padding for left side
    ('RIGHTPADDING', (0, 0), (-1, -1), 10),  # Padding for right side
    ('TOPPADDING', (0, 0), (-1, -1), 5),  # Padding for top side
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # Padding for bottom side
])

    # Create the table and apply the style
    table = Table(data)
    table.setStyle(table_style)

    # Add the table to the document and build it
    elements = [table, NextPageTemplate('main_page_template'), PageBreak()]
    # doc.build(elements)

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
    fig, axis = plt.subplots(nrows=2, ncols=2, figsize=(16, 11))
    axis[0, 0].bar(blood_types, blood_type_counts.values())
    axis[0, 0].set_xlabel('Blood Type')
    axis[0, 0].set_ylabel('Number of Patients')
    axis[0, 0].set_title('Patients by Blood Type')

    # Create the histogram for age distribution
    num_bins = 10
    age_range = (0, 100)
    ages = [patient.get_age for patient in patients]  # Replace 'age' with the correct field name
    axis[0, 1].hist(ages, bins=num_bins, range=age_range, edgecolor='White', color='#005b96')
    axis[0, 1].set_xlabel('Age')
    axis[0, 1].set_ylabel('Number of Patients')
    axis[0, 1].set_title('Patients by Age')

    #
    axis[1,0].pie(gender_type_counts , labels = genders)
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


    # Convert the BytesIO buffer to an image file using PIL
    pil_image = PILImage.open(chart_buffer)

    # Save the PIL image to a temporary file
    temp_image_file = io.BytesIO()
    pil_image.save(temp_image_file, format='png')
    temp_image_file.seek(0)

    # Add the chart to the PDF document
    chart_element = Image(temp_image_file, doc.width, doc.height * 0.5)
    elements = [table, NextPageTemplate('main_page_template'), PageBreak(), chart_element, NextPageTemplate('main_page_template'), PageBreak()]
    doc.build(elements)

    buffer.seek(0)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=patient_list.pdf' + str(datetime.now())+'.pdf'
    # response['Content-Type'] = 'application/pdf' 
    response.write(buffer.getvalue())
    buffer.close()
    

    return response
    # return FileResponse(buffer, as_attachment=True, filename='patient_list.pdf')
