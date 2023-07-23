from django.contrib import admin
from .models import AppUser


class AppUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_superuser', 'is_staff', ]
    list_filter = ['is_superuser', 'is_staff']
    search_fields = ['email']


# Models
admin.site.register(AppUser, AppUserAdmin)
