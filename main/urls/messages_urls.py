"""
URL routing for the Messages module (Kirtan Sodha, Student 3).

Routes:
    /messages/                       -> Inbox (UC-M3)
    /messages/compose/               -> New message form, also handles save draft (UC-M1, UC-M2)
    /messages/compose/?draft=<id>    -> Edit existing draft in compose form (UC-M5)
    /messages/sent/                  -> Sent messages list (UC-M4)
    /messages/drafts/                -> Drafts list (UC-M5)
    /messages/drafts/<id>/delete/    -> Delete a draft (UC-M5)
"""

from django.urls import path
from main.views.messages_views import (
    inbox,
    compose,
    sent,
    drafts,
    delete_draft,
)

urlpatterns = [
    path('', inbox, name='messages'),
    path('compose/', compose, name='messages_compose'),
    path('sent/', sent, name='messages_sent'),
    path('drafts/', drafts, name='messages_drafts'),
    path('drafts/<int:pk>/delete/', delete_draft, name='messages_delete_draft'),
]