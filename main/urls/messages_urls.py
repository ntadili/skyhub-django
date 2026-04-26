"""
URL routing for the Messages module (Kirtan Sodha, Student 3).

The root of /messages/ shows the Inbox. /messages/compose/ is the new-message
form. Additional routes for Sent, Drafts and Read will be added as those
views are built.
"""

from django.urls import path
from main.views.messages_views import inbox, compose

urlpatterns = [
    path('', inbox, name='messages'),
    path('compose/', compose, name='messages_compose'),
]
