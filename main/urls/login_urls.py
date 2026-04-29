from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from main.views.login_views import register

urlpatterns = [
    path(
        '',
        LoginView.as_view(
            template_name='login/login.html',
            redirect_authenticated_user=True,
        ),
        name='login',
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
]
