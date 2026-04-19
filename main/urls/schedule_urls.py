from django.urls import path
from main.views.schedule_views import schedule_page

urlpatterns = [
    path('', schedule_page, name='schedule'),
]