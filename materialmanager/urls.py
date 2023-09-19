from django.urls import path

from . import views

urlpatterns = [
    path('registermaterialmanager/', views.RegisterMaterialManager, name='registermaterialmanager'),
    path('materialmanagerhome/', views.MaterialManagerHome, name='materialmanagerhome'),
    path('announcements/', views.Announcements, name='materialmanagerannouncements'),
    path('updatematerialmanagerprofile/', views.UpdateMaterialManager, name='updatematerialmanagerprofile'),
    path('registermaterial/', views.RegisterMaterial, name='registermaterial'),
    path('searchmaterial/', views.SearchMaterial, name='searchmaterial'),
    path('disposematerial/', views.DisposeMaterial, name='disposematerial'),
    path('material/<str:pk>/', views.Material, name='material'),
    path('servicehistory/<str:pk>/', views.ServiceHistoryMaterial, name='servicehistory'),
    path('relocatematerial/', views.RelocateMaterial, name='relocatematerial'),
    path('servicehistoryform/', views.FillServiceHistroy, name='servicehistoryform'),
    path('materialmanagermessages/', views.MaterialManagerMessages, name='materialmanagermessages'),
    path('messages/<str:pk>/', views.MessagesList, name='materialmanagermessagelist'),

    path('<int:pk>/', views.file_view, name='file_view_material'),
]