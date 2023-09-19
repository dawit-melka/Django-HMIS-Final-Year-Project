from django.contrib import admin
from .models import LabTechnicianProfile, AnatomicalPathologyResult, ProfileTestResult,HematologyResult,BiochemistryTestResult,MicrobiologyResult

admin.site.register(LabTechnicianProfile)
admin.site.register(AnatomicalPathologyResult)
admin.site.register(HematologyResult)
admin.site.register(BiochemistryTestResult)
admin.site.register(MicrobiologyResult)
admin.site.register(ProfileTestResult)
