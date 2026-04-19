from django.urls import path
from main.views.messages_views import messages_page

urlpatterns = [
    path('', messages_page, name='messages'),
]