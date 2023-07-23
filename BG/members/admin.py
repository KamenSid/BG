from django.contrib import admin
from .models import Guild, AppUserProfile


class AppUserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'steam_name', 'steam_id', 'picture', 'guild']
    list_filter = ['guild']
    search_fields = ['username', 'guild__name']


class GuildAdmin(admin.ModelAdmin):
    list_display = ['name', 'leader']
    search_fields = ['name']


admin.site.register(Guild, GuildAdmin)
admin.site.register(AppUserProfile, AppUserProfileAdmin)
