from django.urls import path
from . import views 

urlpatterns = [
    path('registerlabtechnician/', views.RegisterLabTechnician, name='registerlabtechnician'),
    path('labtechnicianhome/', views.LabTechnicianHome, name='labtechnicianhome'),
    path('announcements/', views.Announcements, name='labannouncements'),
    path('labtechnicianupdateprofile/', views.UpdateLabtechnician, name='labtechnicianupdateprofile'),
    path('laborders/', views.LabOrders, name='laborders'),
    path('searchpatients/', views.LabSearchPatients, name='labseacrhpatients'),
    path('labpatientprofile/<str:pk>', views.PatientProfile, name='labpatientprofile'),
    path('laborderandResults/<str:pk>/', views.LabOrderAndResults, name='fromlablaborderandResults'),
    path('labresultform/<str:pk>/', views.LabOrderResultForm, name='labresultform'),
    path('laborderresult/<str:pk>/', views.LabOrderResult, name='laborderresult'),
    path('labmessages/', views.LabMessages, name='labmessages'),
    path('messages/<str:pk>/', views.MessagesList, name='labmessagelist'),
]