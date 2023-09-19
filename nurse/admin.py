from django.contrib import admin

from .models import NurseProfile,VitalSigns,RegisterDeath, RegisterBirth

admin.site.register(NurseProfile)
admin.site.register(VitalSigns)
admin.site.register(RegisterDeath)
admin.site.register(RegisterBirth)

