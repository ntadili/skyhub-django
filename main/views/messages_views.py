"""
Views for the Messages module (Kirtan Sodha, Student 3).

Implements UC-M1 Send Message, UC-M2 Save Draft, UC-M3 View Inbox,
UC-M4 View Sent, UC-M5 View Drafts, UC-M6 Read Message.

This file currently implements UC-M3 (Inbox). Other views will be added
as each use case is built.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.models import Message, Profile


# ---------- helpers ----------

def _get_current_profile(request):
    """Return the Profile linked to the logged-in user, or None if none exists.

    A superuser created via createsuperuser won't have a Profile by default;
    they need one attached before they can send/receive messages.
    """
    try:
        return request.user.profile
    except Profile.DoesNotExist:
        return None


# ---------- UC-M3: View Inbox ----------

@login_required
def inbox(request):
    """Display all non-draft messages where the current user is the recipient.

    Ordering is newest-first (handled by Message.Meta.ordering).
    `select_related('sender')` pre-fetches sender data in the same SQL query,
    avoiding the N+1 query problem on the list rendering.
    """
    my_profile = _get_current_profile(request)

    if my_profile is None:
        messages_list = []
        unread_count = 0
    else:
        messages_list = (
            Message.objects
            .filter(recipient=my_profile, is_draft=False)
            .select_related('sender')
        )
        unread_count = messages_list.filter(status='unread').count()

    context = {
        'messages_list': messages_list,
        'unread_count': unread_count,
        'has_profile': my_profile is not None,
    }
    return render(request, 'messages/inbox.html', context)
