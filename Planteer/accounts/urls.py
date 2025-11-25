from django.urls import path
from . import views  



app_name = "accounts"

urlpatterns = [
    path("sign_up/", views.signup_view, name="sign_up"),
    path("sign_in/", views.signin_view, name="sign_in"),
    path("logout/", views.logout_view, name="logout"),
]