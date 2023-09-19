from django.urls import path
from reception import views

urlpatterns = [
    path('registerreception/', views.RegisterReception, name='registerreception'),
    path('receptionhome/', views.ReceptionHome, name='receptionhome'),
    path('announcements/', views.Announcements, name='receptionannouncements'),
    path('receptionreport/', views.Report, name='receptionreport'),
    path('searchpatients/', views.SearchPatients, name='searchpatients'),
    path('registerpatient/', views.RegisterPatient, name='registerpatient'),
    path('bookappointment/', views.BookAppointment, name='bookappointment'),
    path('bookappointmentfromprofile/<str:pk>', views.BookAppointmentfromProfile, name='bookappointmentfromprofile'),
    path('rescheduleappointment/<str:pk>/', views.RescheduleAppointment, name='rescheduleappointement'),
    path('appointments/', views.Appointments, name='appointments'),
    path('updatereceptionprofile/', views.UpdateReception, name='updatereceptionprofile'),
    path('patientprofile/<str:pk>/', views.PatientProfile, name='patientprofile'),
    path('editpatient/<str:pk>/', views.EditPatient, name='editpatient'),
    path('updatepatient/<str:pk>/', views.UpdatePatient, name='updatepatient'),
    path('receptionmessages/', views.ReceptionMessages, name='receptionmessages'),
    path('messages/<str:pk>/', views.MessagesList, name='receptionmessagelist'),
    path('ajax/load-Doctors/', views.load_Doctors, name='ajax_load_Doctors'),
    path('export-excel', views.export_excel, name="export-excel"),
    path('export-pdf', views.export_pdf, name="export-pdf"),
    
]