from django.contrib import admin

from .models import  UserProfile, Organization, Client, Sensor, ClientRequest, Measurement

class MeasureAdmin(admin.ModelAdmin):
    list_filter = ['sensor']

class SensorAdmin(admin.ModelAdmin):
    list_filter = ['client']
    search_fields = ['sensor']

admin.site.register(UserProfile)
admin.site.register(Client)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(Organization)
admin.site.register(ClientRequest)
admin.site.register(Measurement, MeasureAdmin)
