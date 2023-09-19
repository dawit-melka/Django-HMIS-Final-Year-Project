from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('doctor/',include('doctor.urls')),
    path('reception/',include('reception.urls')),
    path('pharmacist/',include('pharmacist.urls')),
    path('nurse/',include('nurse.urls')),
    path('cashier/',include('cashier.urls')),
    path('radiologist/',include('radiologist.urls')),
    path('labtechnician/',include('labtechnician.urls')),
    path('materialmanager/',include('materialmanager.urls')),
    path('administrator/',include('administrator.urls')),

    path('registerdir/', views.RegisterDir, name='registerdir'),
    path('after-login/', views.afterLogin, name='after-login'),


    path('', views.login_page, name='login'),
    path('logout/', views.LogoutPage, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)