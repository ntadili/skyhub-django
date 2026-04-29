from django.urls import path
from main.views.teams_views import team_list, team_detail

urlpatterns = [
    path('', team_list, name='teams'),
    path('<int:team_id>/', team_detail, name='team_detail'),
]