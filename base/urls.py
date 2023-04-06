from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registerdir/', views.RegisterDir, name='registerdir'),
    path('registerdoctor/', views.RegisterDoctor, name='registerdoctor'),
    path('registerreception/', views.RegisterReception, name='registerreception'),
    path('registerpharmacist/', views.RegisterPharmacist, name='registerpharmacist'),
    ##########################################################################
    path('login/', views.login_page, name='login'),
    ###################################################################################
    path('receptionhome/', views.ReceptionHome, name='receptionhome'),
    path('searchpatients/', views.SearchPatients, name='searchpatients'),
    path('registerpatient/', views.RegisterPatient, name='registerpatient'),
    path('bookappointment/', views.BookAppointment, name='bookappointment'),
    path('bookappointmentfromprofile/<str:pk>', views.BookAppointmentfromProfile, name='bookappointmentfromprofile'),
    path('appointments/', views.Appointments, name='appointments'),
    path('updatereceptionprofile/', views.UpdateReception, name='updatereceptionprofile'),
    path('patientprofile/<str:pk>/', views.PatientProfile, name='patientprofile'),
    path('updatepatient/<str:pk>/', views.UpdatePatient, name='updatepatient'),
    ###################################################################################
    path('doctorhome/', views.DoctorHome, name='doctorhome'),
    path('doctorappointments/', views.DoctorAppointments, name='doctorappointments'),
    path('labhome/', views.LabTech, name='labhome'),
    path('updatedoctorprofile/', views.UpdateDoctor, name='updatedoctorprofile'),
    path('prescribemed/<str:pk>/', views.PrescribeMedicine, name='prescribemed'),
    path('orderlab/<str:pk>/', views.OrderLab, name='orderlab'),
    path('addmedicalhistory/<str:pk>/', views.AddMedicalHistory, name='addmedicalhistory'),
    ######################################################################################
    path('pharmacisthome/', views.PharmacistHome, name='pharmacisthome'),
    path('pharmacistsearch/', views.PharmacistSearchPatients, name='pharmacistseacrhpatients'),
    path('pharmacistupdateprofile/', views.UpdatePharmacist, name='pharmacistupdateprofile'),
    ######################################################################################
    path('logout/', views.LogoutPage, name='logout'),
    path('ajax/load-Doctors/', views.load_Doctors, name='ajax_load_Doctors')
]