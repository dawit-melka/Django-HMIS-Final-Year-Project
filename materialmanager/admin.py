from django.contrib import admin

from .models import MaterialManagerProfile, Manuals, Inventory, InventoryRelocation, ServiceHistory

admin.site.register(MaterialManagerProfile)
admin.site.register(Manuals)
admin.site.register(Inventory)
admin.site.register(InventoryRelocation)
admin.site.register(ServiceHistory)

