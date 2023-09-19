from django.contrib import admin
from .models import DoctorSpecalization, DoctorProfile, LabOrder,PrescribedMedicine, MedicalHistory, RadiologyOrder,BiochemistryTest,ProfileTest,HematologyTest,MicrobiologyTest,AnatomicalPathologyTest,SampleType,Fasting,ImagingType

admin.site.register(DoctorSpecalization)
admin.site.register(DoctorProfile)
admin.site.register(LabOrder)
admin.site.register(PrescribedMedicine)
admin.site.register(RadiologyOrder)
admin.site.register(MedicalHistory)
admin.site.register(BiochemistryTest)
admin.site.register(ProfileTest)
admin.site.register(HematologyTest)
admin.site.register(MicrobiologyTest)
admin.site.register(AnatomicalPathologyTest)
admin.site.register(SampleType)
admin.site.register(Fasting)
admin.site.register(ImagingType)



