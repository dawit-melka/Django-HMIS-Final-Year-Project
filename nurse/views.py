from django.shortcuts import render, redirect,HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import NurseProfileForm, RegistrationForm, VitalSignsForm, RegisterDeathForm, RegisterBirthForm
from django.contrib.auth import login ,logout
from django.db.models import Q
from datetime import datetime, date
from reception.models import Patient, Appointment
from .models import VitalSigns, RegisterDeath, RegisterBirth
from administrator.models import Messaging
from django.contrib.auth.models import User
from administrator.models import Announcement
from doctor.models import DoctorProfile


from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from io import BytesIO

def RegisterNurse(request):
    user_form = RegistrationForm()
    nurse_profile_form = NurseProfileForm()
    
    if request.method == 'POST':
        nurse_profile_form = NurseProfileForm(request.POST, request.FILES)
        user_form = RegistrationForm(request.POST)

        if user_form.is_valid():

            user = user_form.save()

            user.groups.add(3)

            nurse_profile = nurse_profile_form.save(commit=False)
            nurse_profile.nurse = user
            nurse_profile.save()

            login(request,user)
            return redirect('after-login')
    return render(request,'nurse/register.html', {'user_form':user_form, 'profile_form' : nurse_profile_form , 'page': 'Nurse' })

@login_required(login_url='login')
def NurseHome(request):
    doctors_working_now = DoctorProfile.objects.filter(is_working_now=True).count()
    announcements = Announcement.objects.all()[:2]
    return render(request,'nurse/nurse_home.html',{'announcements':announcements, 'doctors_working_now':doctors_working_now})

@login_required(login_url='login')
def Announcements(request):
    announcements = Announcement.objects.all()
    return render(request,'nurse/announcement.html',{'announcements':announcements})

def UpdateNurse(request):
    profile = request.user.nurseprofile
    reception_profile_form = NurseProfileForm(instance=profile)
    
    if request.method == 'POST':
        reception_profile_form = NurseProfileForm(request.POST, request.FILES, instance=profile)

        if reception_profile_form.is_valid():
            reception_profile_form.save()
            return redirect('nursehome')
    return render(request,'nurse/nurse_updateprofile.html', {'profile_form' : reception_profile_form})

@login_required(login_url='login')
def SearchPatients(request):
    search_patient = request.GET.get('search')
    
    if search_patient:
        searched_patients = Patient.objects.filter(Q(first_name__icontains=search_patient) | Q(last_name__icontains=search_patient)
                                | Q(middle_name__icontains=search_patient) | Q(email__icontains=search_patient) | Q(phone__icontains=search_patient))
    else:
        searched_patients=Patient.objects.all()

    return render(request,'nurse/searchpatients.html',{'patients':searched_patients})

@login_required(login_url='login')
def VitalSignsPage(request,pk):
    today = datetime.today().date()

    vitalsignsform = VitalSignsForm()

    patient = Patient.objects.get(id=pk)
    death = None

    if RegisterDeath.objects.filter(Patient = patient):
        death = RegisterDeath.objects.get(Patient = patient)
        dead = True
    else:
        dead = False

    appointments = Appointment.objects.filter(Patient = patient).filter(date=today)
    vitalsigns = VitalSigns.objects.filter(Patient=patient)

    return render(request,"nurse/vitalsigns.html",{'patient':patient , 'appointments': appointments, 'vitalsignsform':vitalsignsform, 'vitalsigns':vitalsigns, 'dead':dead, 'death':death})

@login_required(login_url='login')
def RecordVitalSigns(request,pk):
    patient = Patient.objects.get(id=pk)
    vitalsignsform = VitalSignsForm()
    next = request.POST.get('next', '/')
    if request.method == "POST": 
        vitalsignsform = VitalSignsForm(request.POST)
        if vitalsignsform.is_valid():
            vitalform = vitalsignsform.save(commit=False)
            vitalform.Nurse = request.user.nurseprofile
            vitalform.Patient = patient
            vitalform.save()
            return HttpResponseRedirect(next)
    return render(request,"nurse/recordvitalsigns.html",{'vitalsignsform':vitalsignsform})

@login_required(login_url='login')
def RegisterBirths(request): 

    form = RegisterBirthForm()

    if request.method == "POST": 
        form = RegisterBirthForm(request.POST)
        if form.is_valid():
            birthform = form.save(commit=False)
            birthform.Nurse = request.user.nurseprofile
            birthform.save()

            return redirect('birthregistrations')

    return render(request,"nurse/registerbirth.html", {'form':form})

@login_required(login_url='login')
def BirthRegistrations(request):
    
    birthregistrations = RegisterBirth.objects.all()
    
    search_patient = request.GET.get('search')
    if search_patient:
        birthregistrations = RegisterBirth.objects.filter(Q(Patient__first_name__icontains=search_patient) | Q(Patient__last_name__icontains=search_patient)
                                | Q(Patient__middle_name__icontains=search_patient) | Q(Patient__email__icontains=search_patient) | Q(Patient__phone__icontains=search_patient))

    

    return render(request,'nurse/birthregistrations.html', {'birthregistrations':birthregistrations})


def generate_birth_certificate(request, pk):
    # Retrieve the birth record
    register_birth = RegisterBirth.objects.get(id=pk)

    # Create the PDF document in memory
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name="Title", parent=styles["Heading1"], fontSize=24, alignment=TA_CENTER)
    subtitle_style = ParagraphStyle(name="Subtitle", parent=styles["Heading2"], fontSize=18, alignment=TA_CENTER)
    body_style = styles["BodyText"]

    # Create the content
    content = []

    # Title
    title = Paragraph("Birth Certificate", title_style)
    content.append(title)
    content.append(Spacer(1, 20))

    # Subtitle (Newborn Information)
    subtitle = Paragraph("Newborn Information", subtitle_style)
    content.append(subtitle)
    content.append(Spacer(1, 10))

    # Newborn information table
    newborn_data = [
        ["First Name", register_birth.first_name],
        ["Middle Name", register_birth.middle_name],
        ["Last Name", register_birth.last_name],
        ["Gender", register_birth.gender],
        ["Date of Birth", register_birth.date_of_birth],
        ["Time of Birth", register_birth.time_of_birth],
        ["Birth Weight", f"{register_birth.birth_weight} grams"],
        ["Birth Length", f"{register_birth.birth_length} cm"],
    ]
    newborn_table = Table(newborn_data, colWidths=[3 * inch, 3 * inch])
    newborn_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 7), colors.gray),
        ('TEXTCOLOR', (0, 0), (0, 7), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 13),
    ]))
    content.append(newborn_table)
    content.append(Spacer(2, 20))

    # Subtitle (Parent Information)
    subtitle = Paragraph("Parent Information", subtitle_style)
    content.append(subtitle)
    content.append(Spacer(2, 10))

    # Parent information table
    parent_data = [
        ["Mother's Name", f"{register_birth.mother_first_name} {register_birth.mother_middle_name} {register_birth.mother_last_name}"],
        ["Mother's Date of Birth", register_birth.mother_date_of_birth],
        ["Mother's Nationality", register_birth.mother_nationality],
        ["Mother's Occupation", register_birth.mother_occupation],
        ["Father's Name", f"{register_birth.father_first_name} {register_birth.father_middle_name} {register_birth.father_last_name}"],
        ["Father's Date of Birth", register_birth.father_date_of_birth],
        ["Father's Nationality", register_birth.father_nationality],
        ["Father's Occupation", register_birth.father_occupation],
    ]
    parent_table = Table(parent_data, colWidths=[3 * inch, 3 * inch])
    parent_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 7), colors.gray),
        ('TEXTCOLOR', (0, 0), (0, 7), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 13),
    ]))
    content.append(parent_table)

    # Build the PDF
    doc.build(content)

    # Retrieve the PDF from the buffer
    pdf = buffer.getvalue()
    buffer.close()

    # Prepare the response with the generated PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="birth_certificate_{register_birth.id}.pdf"'
    response.write(pdf)

    return response

@login_required(login_url='login')
def BabyInfoPage(request,pk):

    baby = RegisterBirth.objects.get(id=pk)

    return render(request,"nurse/babyinfo.html",{'baby':baby})


@login_required(login_url='login')
def RegisterDeaths(request):
    registerdeathform = RegisterDeathForm()
    if request.method == "POST": 
        registerdeathform = RegisterDeathForm(request.POST)
        patient_id = request.POST.get('patient')
        if registerdeathform.is_valid():
            deathform = registerdeathform.save(commit=False)
            deathform.Nurse = request.user.nurseprofile
            deathform.Patient = Patient.objects.get(id=patient_id)
            deathform.save()
            return redirect('vitalsigns', patient_id)
    return render(request,"nurse/registerdeath.html",{'registerdeathform':registerdeathform})

@login_required(login_url='login')
def DeadPatients(request):
    search_patient = request.GET.get('search')
    
    if search_patient:
        searched_patients = RegisterDeath.objects.filter(Q(first_name__icontains=search_patient) | Q(last_name__icontains=search_patient)
                                | Q(middle_name__icontains=search_patient) | Q(email__icontains=search_patient) | Q(phone__icontains=search_patient))
    else:
        searched_patients=RegisterDeath.objects.all()

    return render(request,'nurse/deadpatients.html',{'deadpatients':searched_patients})

@login_required(login_url='login')
def NurseAppointments(request):
    
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
    return render(request,'nurse/nurse_appointment.html', {'appointments':appointments})


@login_required(login_url='login')
def NurseMessages(request):
   

    chats = User.objects.all()

    array = []
    staffs = User.objects.all()
    for staff in staffs:
        chatcount = Messaging.objects.filter(sender=staff, receiver=request.user, seen = False)
        array.append(chatcount.count())
    
    zipped =zip(chats,array)

    context = {'chats':chats, 'array':array, 'zipped':zipped}
    
    return render(request,"nurse/messages/messages_base.html", context)

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
    
        return redirect('nursemessagelist', pk=user.id)


    context = {'chats':chats, 'messageslist': messageslist, 'user':user, 'zipped':zipped}

    return render(request,"nurse/messages/messages.html", context)