from django.urls import path

from . import views

urlpatterns = [
    path('registercashier/', views.RegisterCashier, name='registercashier'),
    path('cashierhome/', views.CashierHome, name='cashierhome'),
    path('announcements/', views.Announcements, name='cashierannouncements'),
    path('updatecashierprofile/', views.UpdateCashier, name='updatecashierprofile'),
    path('receptionreport/', views.Report, name='cashierreport'),
    path('payments/', views.Payments, name='payments'),
    path('pharmapayments/', views.PharmaPayments, name='pharmapayments'),
    path('searchpatients/', views.SearchPatients, name='cashiersearchpatients'),
    path('patientprofile/<str:pk>', views.PatientProfile, name='cashierpatientprofile'),
    path('fullappointment/<str:pk>', views.FullAppointment, name='fullappointment'),
    path('fulllaborder/<str:pk>', views.FullLabOrder, name='fulllaborder'),
    path('fullradiologyorder/<str:pk>', views.FullRadiologyOrder, name='fullradiologyorder'),
    path('fullmed/<str:pk>', views.FullMed, name='fullmed'),
    path('cashiermessages/', views.CashierMessages, name='cashiermessages'),
    path('messages/<str:pk>/', views.MessagesList, name='cashiermessagelist'),
    path('export-excel', views.export_excel, name="banalcesheet-export-excel"),
]