"""
URL routing for the Messages module (Kirtan Sodha, Student 3).

Routes:
    /messages/         -> Inbox (UC-M3)
    /messages/compose/ -> New message form, also handles save draft (UC-M1, UC-M2)
    /messages/sent/    -> Sent messages list (UC-M4)
"""

from django.urls import path
from main.views.messages_views import inbox, compose, sent

urlpatterns = [
    path('', inbox, name='messages'),
    path('compose/', compose, name='messages_compose'),
    path('sent/', sent, name='messages_sent'),
]