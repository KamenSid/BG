from django.contrib import admin
from .models import Replay


class ReplayAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'game', ]
    list_filter = ['author', 'game']
    search_fields = ['title', 'author__appuserprofile__username', 'game']


# Models
admin.site.register(Replay, ReplayAdmin)
