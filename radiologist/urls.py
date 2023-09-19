from django.urls import path
from . import views 

urlpatterns = [
    path('registerradiologist/', views.RegisterRadiologist, name='registerradiologist'),
    path('radiologisthome/', views.RadiologistHome, name='radiologisthome'),
    path('announcements/', views.Announcements, name='radiologistannouncements'),
    path('radiologyorder/', views.RadiologyOrders, name='radiologistorder'),
    path('radiologistsearch/', views.RadiologistSearchPatients, name='radiologistseacrhpatients'),
    path('radiologistpatientprofile/<str:pk>', views.PatientProfile, name='radiologistpatientprofile'),
    path('radiologyresultform/<str:pk>', views.RadiologyResultForm, name='radiologyresultform'),
    path('radiologyresult/<str:pk>', views.RadiologyResults, name='radiologyresult'),
    path('radiologistupdateprofile/', views.UpdateRadiologist, name='radiologistupdateprofile'),
    path('radiologistmessages/', views.RadiologistMessages, name='radiologistmessages'),
    path('messages/<str:pk>/', views.MessagesList, name='radiologistmessagelist'),

    path('<int:pk>/', views.file_view, name='file_view'),
]