from django.urls import path

from . import views

urlpatterns = [
    path('adminhome/', views.AdminHome, name='adminhome'),
    path('updateadminprofile/', views.UpdateAdmin, name='updateadminprofile'),
    path('approverequests/', views.ApproveRequests, name='approverequests'),
    path('searchstaff/', views.SearchStaff, name='searchstaff'),
    path('announcements/', views.Announcements, name='announcements'),
    path('createannouncements/', views.CreateAnnouncements, name='createannouncements'),
    # path('administratorreport/', views.Report, name='administratorreport'),
    
    path('patientsreport/', views.PatientsReport, name='patientsreport'),
    path('staffsreport/', views.StaffsReport, name='staffsreport'),
    path('financialreport/', views.FinancialReport, name='financialreport'),
    path('export-excel', views.export_excel, name="banalcesheet-export-excel"),

    
    path('approvedoctor/<str:pk>/', views.ApproveDoctor, name='approvedoctor'),
    path('approvecashier/<str:pk>/', views.ApproveCashier, name='approvecashier'),
    path('approvereception/<str:pk>/', views.ApproveReception, name='approvereception'),
    path('approvenurse/<str:pk>/', views.ApproveNurse, name='approvenurse'),
    path('approverpharma/<str:pk>/', views.ApprovePharmacist, name='approverpharma'),
    path('approveradiologist/<str:pk>/', views.ApproveRadiologist, name='approveradiologist'),
    path('approvedlab/<str:pk>/', views.ApproveLab, name='approvedlab'),
    path('approvematerial/<str:pk>/', views.ApproveMaterial, name='approvematerial'),

    path('deletedoctor/<str:pk>/', views.DeleteDoctor, name='deletedoctor'),
    path('deletecashier/<str:pk>/', views.DeleteCashier, name='deletecashier'),
    path('deletereception/<str:pk>/', views.DeleteReception, name='deletereception'),
    path('deletenurse/<str:pk>/', views.DeleteNurse, name='deletenurse'),
    path('deletepharma/<str:pk>/', views.DeletePharmacist, name='deletepharma'),
    path('deleteradiologist/<str:pk>/', views.DeleteRadiologist, name='deleteradiologist'),
    path('deletelab/<str:pk>/', views.DeleteLab, name='deletelab'),
    path('deletematerial/<str:pk>/', views.DeleteMaterial, name='deletematerial'),

    path('adminmessages/', views.AdminMessages, name='adminmessages'),
    path('messages/<str:pk>/', views.MessagesList, name='adminmessagelist'),
    
]