from django.urls import path
from main.views.login_views import login_view

urlpatterns = [
    path('', login_view, name='login'),
]