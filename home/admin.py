from django.contrib import admin
from .models import CustomUser, Client, Caregiver, CareManager
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Client)
admin.site.register(Caregiver)
admin.site.register(CareManager)