from django.urls import path

from main.views.settings_views import settings_index

urlpatterns = [
    path('', settings_index, name='settings'),
]
