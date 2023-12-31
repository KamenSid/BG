from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include
from BG.members.views import ReplayDetailAPIView, ReplayListAPIView, replay_list_frontend_view
from BG.testdb.views import IndexView, error_404, error_500

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('admin/', admin.site.urls),
    path('testdb/', include('BG.testdb.urls')),
    path('accounts/', include('BG.accounts.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('BG.members.urls')),

    # API URLS

    path("API/", include([
        path('replays/<int:pk>/', ReplayDetailAPIView.as_view()),
        path('replays/', ReplayListAPIView.as_view(), name='replay-list-API'),
        path('replays/front/', replay_list_frontend_view, name='replay-list-API'), ])
         ),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Setup of the custom admin site
admin.site.site_header = "BG Admin"
admin.site.site_title = "BiGGameS Admin Portal"
admin.site.index_title = "Welcome to BiGGameS"

# Setup of the custom 404 and 500 pages.
handler404 = error_404
handler500 = error_500
