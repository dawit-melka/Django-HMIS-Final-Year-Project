from django.urls import path

from . import views

urlpatterns = [
    path('registerpharmacist/', views.RegisterPharmacist, name='registerpharmacist'),
    path('pharmacisthome/', views.PharmacistHome, name='pharmacisthome'),
    path('announcements/', views.Announcements, name='pharmacistannouncements'),
    path('pharmacistsearch/', views.PharmacistSearchPatients, name='pharmacistseacrhpatients'),
    path('pharmacistupdateprofile/', views.UpdatePharmacist, name='pharmacistupdateprofile'),
    path('prescribedmedicines/<str:pk>', views.PrescribedMedicines, name='prescribedmedicines'),
    path('pharmacistmessages/', views.PharmacistMessages, name='pharmacistmessages'),
    path('messages/<str:pk>/', views.MessagesList, name='pharmacistmessagelist'),
]