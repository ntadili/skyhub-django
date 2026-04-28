from django.urls import path
from main.views.dashboard_views import dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
]