
from django.contrib import admin
from django.urls import path
from django.urls import include

import BG.testdb.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name="index"),
    path('testdb/', include('BG.testdb.urls')),
    path('accounts/', include('BG.accounts.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('BG.members.urls')),
]