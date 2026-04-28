from django.urls import path
from main.views.teams_views import team_list

urlpatterns = [
    path('', team_list, name='teams'),
]