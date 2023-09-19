from django.contrib import admin

from .models import Messaging, AdminProfile,Announcement

admin.site.register(Messaging)

admin.site.register(AdminProfile)

admin.site.register(Announcement)
