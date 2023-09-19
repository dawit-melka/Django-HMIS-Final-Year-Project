from django.urls import path
from doctor import views

urlpatterns = [
    path('', views.DoctorHome, name='doctorhome'),
    path('registerdoctor/', views.RegisterDoctor, name='registerdoctor'),
    path('announcements/', views.Announcements, name='doctorannouncements'),
    path('schedulecheckup/', views.ScheduleCheckup, name='schedulecheckup'),
    path('bookappointmentfromprofile/<str:pk>', views.BookAppointmentfromProfile, name='bookappointmentfromdoctor'),
    path('doctorappointments/', views.DoctorAppointments, name='doctorappointments'),
    path('updatedoctorprofile/', views.UpdateDoctor, name='updatedoctorprofile'),
    path('prescribemed/<str:pk>/', views.PrescribeMedicine, name='prescribemed'),
    path('radiologyorder/<str:pk>/', views.RadiologyOrderPage, name='radiologyorder'),
    path('orderlab/<str:pk>/', views.OrderLab, name='orderlab'),
    path('laborderandResults/<str:pk>/', views.LabOrderAndResults, name='doclaborderandResults'),
    path('laborderresult/<str:pk>/', views.LabOrderResult, name='doclaborderresult'),
    path('addmedicalhistory/<str:pk>/', views.AddMedicalHistory, name='addmedicalhistory'),
    path('searchpatients/', views.SearchPatients, name='doctorsearchpatients'),
    path('patientprofile/<str:pk>/', views.PatientProfile, name='doctorpatientprofile'),
    path('vitalsigns/<str:pk>/', views.VitalSignsPage, name='doctorvitalsigns'),
    path('patienthistory/<str:pk>/', views.PatientHistory, name='patienthistory'),
    path('patientlabhistory/<str:pk>/', views.PatientLabHistory, name='patientlabhistory'),
    path('patientlprescriptionhistory/<str:pk>/', views.PatientPrescriptionHistory, name='patientlprescriptionhistory'),
    path('patientlradiologyhistory/<str:pk>/', views.PatientRadiologyHistory, name='patientradiologyhistory'),
    path('radiologyresult/<str:pk>', views.RadiologyResults, name='doctorradiologyresult'),
    path('doctormessages/', views.DoctorMessages, name='doctormessages'),
    path('messages/<str:pk>/', views.MessagesList, name='doctormessagelist'),

    path('<int:pk>/', views.file_view, name='file_view'),
]