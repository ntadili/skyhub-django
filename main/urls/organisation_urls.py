from django.urls import path
from main.views.organisation_views import organisation_page

urlpatterns = [
    path('', organisation_page, name='organisation'),
]