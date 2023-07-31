from django.urls import path

from BG.testdb import views

urlpatterns = (


    path("search/", views.SearchView.as_view(), name="search"),
)
