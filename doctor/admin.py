from django.contrib import admin
from .models import Appointment, Profile
# Register your models here.

admin.site.register(Appointment)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "phone", "country")