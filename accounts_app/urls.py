from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import registerUser

urlpatterns = [
    path("login/", LoginView.as_view(template_name="accounts_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="accounts_app/logout.html"), name="logout"),
    path("register/", registerUser, name="register"),
]
