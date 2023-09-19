from django.shortcuts import render, redirect, HttpResponse
from .forms import CashierProfileForm,RegistrationForm,ExcelForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from reception.models import Appointment,Patient
from django.db.models import Q 
from administrator.models import Messaging,Announcement
from django.contrib.auth.models import User
from doctor.models import LabOrder, RadiologyOrder, PrescribedMedicine
import xlwt
from datetime import datetime, date

def RegisterCashier(request):
    user_form = RegistrationForm()
    cashier_profile_form = CashierProfileForm()
    
    if request.method == 'POST':
        cashier_profile_form = CashierProfileForm(request.POST, request.FILES)
        user_form = RegistrationForm(request.POST)

        if user_form.is_valid():

            user = user_form.save()

            user.groups.add(2)

            cashier_profile = cashier_profile_form.save(commit=False)
            cashier_profile.cashier = user
            cashier_profile.save()

            login(request,user)
            return redirect('after-login')
    return render(request,'cashier/register.html', {'user_form':user_form, 'profile_form' : cashier_profile_form , 'page': 'Cashier' })


@login_required(login_url='login')
def CashierHome(request):
    announcements = Announcement.objects.all()[:2]
    appointments = Appointment.objects.filter(payment = False , status = True).count()
    laborder = LabOrder.objects.filter(payment = False).count()
    radiologyorder = RadiologyOrder.objects.filter(payment = False).count()

    payments = appointments + laborder + radiologyorder


    return render(request,'cashier/cashier_home.html',{'announcements':announcements, 'payments': payments})

@login_required(login_url='login')
def Announcements(request):
    announcements = Announcement.objects.all()
    return render(request,'cashier/announcement.html',{'announcements':announcements})

@login_required(login_url='login')
def UpdateCashier(request):
    profile = request.user.cashierprofile
    cashier_profile_form = CashierProfileForm(instance=profile)
    
    if request.method == 'POST':
        cashier_profile_form = CashierProfileForm(request.POST, request.FILES, instance=profile)

        if cashier_profile_form.is_valid():
            cashier_profile_form.save()
            return redirect('cashierhome')
    return render(request,'cashier/cashier_updateprofile.html', {'profile_form' : cashier_profile_form})

from operator import attrgetter

@login_required(login_url='login')
def Report(request):
    form = ExcelForm()

    return render(request,'cashier/reports.html',{'form':form   })

@login_required(login_url='login')
def Payments(request):
    appointments = Appointment.objects.filter(payment = False , status = True)
    laborder = LabOrder.objects.filter(payment = False)
    radiologyorder = RadiologyOrder.objects.filter(payment = False)

    payments = sorted(
        [*appointments, *laborder, *radiologyorder],
        key=attrgetter('created'),
        reverse=True
    )

    
    search_patient = request.GET.get('search')
    if search_patient:
        appointments = Appointment.objects.filter(Q(Patient__first_name__icontains=search_patient) | Q(Patient__last_name__icontains=search_patient)
                                | Q(Patient__middle_name__icontains=search_patient) | Q(Patient__email__icontains=search_patient) | Q(Patient__phone__icontains=search_patient)).filter(payment = False , status = True)
        laborder = LabOrder.objects.filter(Q(Patient__first_name__icontains=search_patient) | Q(Patient__last_name__icontains=search_patient)
                                | Q(Patient__middle_name__icontains=search_patient) | Q(Patient__email__icontains=search_patient) | Q(Patient__phone__icontains=search_patient)).filter(payment = False)
        radiologyorder = RadiologyOrder.objects.filter(Q(Patient__first_name__icontains=search_patient) | Q(Patient__last_name__icontains=search_patient)
                                | Q(Patient__middle_name__icontains=search_patient) | Q(Patient__email__icontains=search_patient) | Q(Patient__phone__icontains=search_patient)).filter(payment = False)
        
        payments = sorted(
            [*appointments, *laborder, *radiologyorder],
            key=attrgetter('created'),
            reverse=True
        )


    if request.method == 'POST' and request.POST.get('payment_id'):
        payment_id =request.POST.get('payment_id')

        try:
            appointment  = Appointment.objects.get(id=payment_id)
            if appointment is not None:
                if appointment.payment == False:
                    appointment.payment=True
                    appointment.Cashier = request.user.cashierprofile
                    appointment.payment_date= date.today()
                    appointment.save()
                    return redirect('payments')
                
                    
        except:
            pass

        try:
            laborder = LabOrder.objects.get(id=payment_id)
            if laborder is not None:
                if laborder.payment == False:
                    laborder.payment=True
                    laborder.Cashier = request.user.cashierprofile
                    laborder.payment_date= date.today()
                    laborder.save()
                    return redirect('payments')
                
        except:
            pass

        try:
            radiologyorder = RadiologyOrder.objects.get(id=payment_id)
            if radiologyorder is not None:
                if radiologyorder.payment == False:
                    radiologyorder.payment=True
                    radiologyorder.Cashier = request.user.cashierprofile
                    radiologyorder.payment_date= date.today()
                    radiologyorder.save()
                    return redirect('payments')
                
        except:
            pass
        
    return render(request,'cashier/payments.html', {'payments':payments})

@login_required(login_url='login')
def PharmaPayments(request):
    medicines = PrescribedMedicine.objects.filter(payment = False)
    
    search_patient = request.GET.get('search')
    if search_patient:
        medicines = PrescribedMedicine.objects.filter(Q(Patient__first_name__icontains=search_patient) | Q(Patient__last_name__icontains=search_patient)
                                | Q(Patient__middle_name__icontains=search_patient) | Q(Patient__email__icontains=search_patient) | Q(Patient__phone__icontains=search_patient)).filter(payment = False)

    if request.method == 'POST' and request.POST.get('payment_id'):
        payment_id =request.POST.get('payment_id')

        medicine  = PrescribedMedicine.objects.get(id=payment_id)

        if medicine.payment == False:
            medicine.payment=True
            medicine.Cashier = request.user.cashierprofile
            medicine.payment_date= date.today()
            medicine.save()
            return redirect('pharmapayments')
                    
        
    return render(request,'cashier/pharma_payments.html', {'medicines':medicines})


@login_required(login_url='login')
def SearchPatients(request):
    search_patient = request.GET.get('search')
    
    if search_patient:
        searched_patients = Patient.objects.filter(Q(first_name__icontains=search_patient) | Q(last_name__icontains=search_patient)
                                | Q(middle_name__icontains=search_patient) | Q(email__icontains=search_patient) | Q(phone__icontains=search_patient))
    else:
        searched_patients=Patient.objects.all()
    
    return render(request,'cashier/searchpatients.html',{'patients':searched_patients})


@login_required(login_url='login')
def PatientProfile(request,pk):

    patient = Patient.objects.get(id=pk)
    appointments = Appointment.objects.filter(Patient = patient)[:5]
    laborders = LabOrder.objects.filter(Patient = patient)[:5]
    radiologyorders = RadiologyOrder.objects.filter(Patient = patient)[:5]
    medicines = PrescribedMedicine.objects.filter(Patient = patient)[:5]

    if request.method == 'POST' and request.POST.get('appointment_id'):
        appointment_id =request.POST.get('appointment_id')
        appointment  = Appointment.objects.get(id=appointment_id)
        if appointment.payment == False:
            appointment.payment=True
            appointment.Cashier = request.user.cashierprofile
            appointment.payment_date= date.today()
            appointment.save()
        else:
            appointment.payment = False
            appointment.save()

    if request.method == 'POST' and request.POST.get('laborder_id'):
        laborder_id =request.POST.get('laborder_id')
        laborder  = LabOrder.objects.get(id=laborder_id)
        if laborder.payment == False:
            laborder.payment=True
            laborder.Cashier = request.user.cashierprofile
            laborder.payment_date= date.today()
            laborder.save()
        else:
            laborder.payment = False
            laborder.save()

    if request.method == 'POST' and request.POST.get('radiologyorder_id'):
        radiologyorder_id =request.POST.get('radiologyorder_id')
        radiologyorder  = RadiologyOrder.objects.get(id=radiologyorder_id)
        if radiologyorder.payment == False:
            radiologyorder.payment=True
            radiologyorder.Cashier = request.user.cashierprofile
            radiologyorder.payment_date= date.today()
            radiologyorder.save()
        else:
            radiologyorder.payment = False
            radiologyorder.save()

    if request.method == 'POST' and request.POST.get('medicine_id'):
        medicine_id =request.POST.get('medicine_id')
        medicine  = PrescribedMedicine.objects.get(id=medicine_id)
        if medicine.payment == False:
            medicine.payment=True
            medicine.Cashier = request.user.cashierprofile
            medicine.save()
        else:
            medicine.payment = False
            medicine.save()
    return render(request,"cashier/patientprofile.html",{'patient':patient, 'appointments': appointments, 'laborders':laborders, 'radiologyorders':radiologyorders, 'medicines':medicines })

@login_required(login_url='login')
def FullAppointment(request,pk):

    patient = Patient.objects.get(id=pk)
    appointments = Appointment.objects.filter(Patient = patient)


    if request.method == 'POST' and request.POST.get('appointment_id'):
        appointment_id =request.POST.get('appointment_id')
        appointment  = Appointment.objects.get(id=appointment_id)
        if appointment.payment == False:
            appointment.payment=True
            appointment.Cashier = request.user.cashierprofile
            appointment.payment_date= date.today()
            appointment.save()
        else:
            appointment.payment = False
            appointment.save()

    return render(request,"cashier/fullappointment.html",{'patient':patient, 'appointments': appointments})

@login_required(login_url='login')
def FullLabOrder(request,pk):

    patient = Patient.objects.get(id=pk)
    laborders = LabOrder.objects.filter(Patient = patient)


    if request.method == 'POST' and request.POST.get('laborder_id'):
        laborder_id =request.POST.get('laborder_id')
        laborder  = LabOrder.objects.get(id=laborder_id)
        if laborder.payment == False:
            laborder.payment=True
            laborder.Cashier = request.user.cashierprofile
            laborder.payment_date= date.today()
            laborder.save()
        else:
            laborder.payment = False
            laborder.save()

    return render(request,"cashier/fulllab.html",{'patient':patient,'laborders':laborders})

@login_required(login_url='login')
def FullRadiologyOrder(request,pk):

    patient = Patient.objects.get(id=pk)
    radiologyorders = RadiologyOrder.objects.filter(Patient = patient)

    if request.method == 'POST' and request.POST.get('radiologyorder_id'):
        radiologyorder_id =request.POST.get('radiologyorder_id')
        radiologyorder  = Appointment.objects.get(id=radiologyorder_id)
        if radiologyorder.payment == False:
            radiologyorder.payment=True
            radiologyorder.Cashier = request.user.cashierprofile
            radiologyorder.payment_date= date.today()
            radiologyorder.save()
        else:
            radiologyorder.payment = False
            radiologyorder.save()

    return render(request,"cashier/fullradiology.html",{'patient':patient, 'radiologyorders':radiologyorders })

@login_required(login_url='login')
def FullMed(request,pk):

    patient = Patient.objects.get(id=pk)
    medicines = PrescribedMedicine.objects.filter(Patient = patient)[:5]

    if request.method == 'POST' and request.POST.get('medicine_id'):
        medicine_id =request.POST.get('medicine_id')
        medicine  = PrescribedMedicine.objects.get(id=medicine_id)
        if medicine.payment == False:
            medicine.payment=True
            medicine.Cashier = request.user.cashierprofile
            medicine.payment_date= date.today()
            medicine.save()
        else:
            medicine.payment = False
            medicine.save()

    return render(request,"cashier/fullmed.html",{'patient':patient, 'medicines':medicines })

@login_required(login_url='login')
def CashierMessages(request):
   

    chats = User.objects.all()

    array = []
    staffs = User.objects.all()
    for staff in staffs:
        chatcount = Messaging.objects.filter(sender=staff, receiver=request.user, seen = False)
        array.append(chatcount.count())
    
    zipped =zip(chats,array)

    context = {'chats':chats, 'array':array, 'zipped':zipped}
    
    return render(request,"cashier/messages/messages_base.html", context)

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
    
        return redirect('cashiermessagelist', pk=user.id)


    context = {'chats':chats, 'messageslist': messageslist, 'user':user, 'zipped':zipped}

    return render(request,"cashier/messages/messages.html", context)

def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-disposition'] = 'attachment; filename=Patients_List'+ \
        str(datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Patient List')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Patient id','Patient Name','Type', 'Doctor(appointment doctor /orderd by)', 'Creation Date', 'Price']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()
    
    appointments = Appointment.objects.filter(payment = True, Cashier = request.user.cashierprofile)
    laborder = LabOrder.objects.filter(payment = True, Cashier = request.user.cashierprofile)
    radiologyorder = RadiologyOrder.objects.filter(payment = True, Cashier = request.user.cashierprofile)

    payments = sorted(
        [*appointments, *laborder, *radiologyorder],
        key=attrgetter('payment_date'),
        reverse=True
    )

    for payment in payments:
        type = 'Appointment'
        try:
            if payment.radio:
                type = 'Radiology'
        except:
            try:
                if payment.lab:
                    type = 'Lab'
            except:
                pass
         

        row_num += 1
        ws.write(row_num, 0, str(payment.Patient.id))
        ws.write(row_num, 1, str(payment.Patient.first_name))
        ws.write(row_num, 2, str(type))
        ws.write(row_num, 3, str(payment.Doctor))
        ws.write(row_num, 4, str(payment.created))
        ws.write(row_num, 5, str(payment.total_price))

    wb.save(response)
    return response