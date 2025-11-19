from . import views
from django.urls import path

app_name = "home"

urlpatterns = [
    path("", views.home_page, name="home_page"),
]