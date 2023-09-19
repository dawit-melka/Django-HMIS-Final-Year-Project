from django.urls import path
from . import views

urlpatterns = [
    path('registerreception/', views.RegisterNurse, name='registernurse'),
    path('nursehome/', views.NurseHome, name='nursehome'),
    path('announcements/', views.Announcements, name='nurseannouncements'),
    path('updatenurseprofile/', views.UpdateNurse, name='updatenurseprofile'),
    path('vitalsignregistersearch', views.SearchPatients, name='vitalsignregistersearch'),
    path('vitalsigns/<str:pk>/', views.VitalSignsPage, name='vitalsigns'),
    path('recordvitalsigns/<str:pk>/', views.RecordVitalSigns, name='recordvitalsigns'),
    path('registerbirth/', views.RegisterBirths, name='registerbirth'),
    path('birthcertificate/<str:pk>/', views.generate_birth_certificate,name= 'birthcertificate'),
    path('registerdeath/', views.RegisterDeaths, name='registerdeath'),
    path('deadpatients/', views.DeadPatients, name='deadpatients'),
    path('nurseappointments/', views.NurseAppointments, name='nurseappointments'),
    path('birthregistrations/', views.BirthRegistrations, name='birthregistrations'),
    path('babyinfo/<str:pk>/', views.BabyInfoPage, name='babyinfo'),
    path('nursemessages/', views.NurseMessages, name='nursemessages'),
    path('messages/<str:pk>/', views.MessagesList, name='nursemessagelist'),
]