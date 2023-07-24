from django.contrib import admin
from .models import AppUser


class AppUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_superuser', 'is_staff', ]
    list_filter = ['is_superuser', 'is_staff']
    search_fields = ['email']
    fieldsets = (
        ('Registration information', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': (
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )}),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)


# Models
admin.site.register(AppUser, AppUserAdmin)
