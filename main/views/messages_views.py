"""
Views for the Messages module (Kirtan Sodha, Student 3).

Implements UC-M1 Send Message, UC-M2 Save Draft, UC-M3 View Inbox,
UC-M4 View Sent, UC-M5 View Drafts, UC-M6 Read Message.

Currently implements: UC-M3 (Inbox), UC-M1 (Send), UC-M2 (Save Draft).
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages

from main.models import Message, Profile


# ---------- helpers ----------

def _get_current_profile(request):
    """Return the Profile linked to the logged-in user, or None if none exists.

    A superuser created via createsuperuser won't have a Profile by default;
    they need one attached via the admin panel before they can send/receive.
    """
    try:
        return request.user.profile
    except Profile.DoesNotExist:
        return None


# ---------- UC-M3: View Inbox ----------

@login_required
def inbox(request):
    """Display all non-draft messages where the current user is the recipient.

    Ordering is newest-first (from Message.Meta.ordering).
    select_related('sender') pre-fetches the sender in one SQL query,
    avoiding the N+1 query problem when rendering the list.
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


# ---------- UC-M1: Send Message  /  UC-M2: Save Draft ----------

@login_required
def compose(request):
    """Compose a new message and either send it or save it as a draft.

    GET  -> empty form.
    POST -> validate and create a Message. The `action` field on the submitted
            form tells us whether this is a Send (action=send) or Save Draft
            (action=save_draft). Validation rules differ between the two.

    Covers test cases TC-M1-01 .. TC-M1-04 and TC-M2-01 .. TC-M2-02.

    Note on the `errors` dict: keys are field names ('recipient', 'subject',
    'body') plus a catch-all key 'form_error' for errors that don't attach to
    a specific field. We avoid Django's convention of '__all__' because
    Django's template language disallows variable names starting with '_'.
    """
    my_profile = _get_current_profile(request)

    if my_profile is None:
        django_messages.warning(
            request,
            "Your account has no Profile yet — add one in the admin before composing."
        )
        return redirect('messages')

    # Everyone except me. Ordered for a stable dropdown.
    recipients = (
        Profile.objects
        .exclude(pk=my_profile.pk)
        .order_by('first_name', 'last_name')
    )

    errors = {}
    form_data = {'recipient': '', 'subject': '', 'body': ''}

    if request.method == 'POST':
        recipient_id = request.POST.get('recipient', '').strip()
        subject = request.POST.get('subject', '').strip()
        body = request.POST.get('body', '').strip()
        action = request.POST.get('action', '')

        # Keep submitted values so the form re-renders with them on error.
        form_data = {
            'recipient': recipient_id,
            'subject': subject,
            'body': body,
        }

        # --- validation ---
        if action == 'send':
            if not recipient_id:
                errors['recipient'] = 'Recipient is required.'
            if not body:
                errors['body'] = 'Message body is required.'
        elif action == 'save_draft':
            # Draft allows a blank subject; but there must be SOME content
            # to save (otherwise there's nothing meaningful to persist).
            if not subject and not body:
                errors['form_error'] = 'Write a subject or body before saving as draft.'
        else:
            errors['form_error'] = 'Unknown action.'

        if len(subject) > 255:
            errors['subject'] = 'Subject cannot exceed 255 characters.'

        # Guard against tampered recipient values
        recipient = None
        if recipient_id:
            try:
                recipient = recipients.get(pk=recipient_id)
            except Profile.DoesNotExist:
                errors['recipient'] = 'Selected recipient does not exist.'

        # --- on success, create the Message and redirect ---
        if not errors:
            is_draft = (action == 'save_draft')
            Message.objects.create(
                sender=my_profile,
                recipient=recipient,  # may be None for drafts
                subject=subject,
                body=body,
                is_draft=is_draft,
            )
            if is_draft:
                django_messages.success(request, 'Draft saved.')
            else:
                django_messages.success(request, 'Message sent.')
            return redirect('messages')

    context = {
        'recipients': recipients,
        'errors': errors,
        'form_data': form_data,
    }
    return render(request, 'messages/compose.html', context)
