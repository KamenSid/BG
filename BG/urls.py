
from django.contrib import admin
from django.urls import path
from django.urls import include

import BG.testdb.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', BG.testdb.views.index, name="index"),
    path('testdb/', include('BG.testdb.urls')),
    path('accounts/', include('BG.accounts.urls'), name="accounts"),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('BG.members.urls'), name="members"),
]
