from django.contrib import admin
from .models import Patient, Appointment, DoctorSpecalization, DoctorProfile,ReceptionProfile,LabOrder,PrescribedMedicine,MedicalHistory, PharmacistProfile

admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(DoctorSpecalization)
admin.site.register(DoctorProfile)
admin.site.register(ReceptionProfile)
admin.site.register(LabOrder)
admin.site.register(PrescribedMedicine)
admin.site.register(MedicalHistory)
admin.site.register(PharmacistProfile)
