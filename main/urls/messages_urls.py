"""
URL routing for the Messages module (Kirtan Sodha, Student 3).

The root of /messages/ shows the Inbox. Additional routes for Sent, Drafts,
Compose and Read will be added as those views are built.
"""

from django.urls import path
from main.views.messages_views import inbox

urlpatterns = [
    path('', inbox, name='messages'),
]
