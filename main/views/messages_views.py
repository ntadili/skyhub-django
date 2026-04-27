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


# ---------- UC-M1: Send Message  /  UC-M2: Save Draft  /  UC-M5 (edit draft) ----------

@login_required
def compose(request):
    """Compose a new message, send it, save it as a draft, or edit an existing draft.

    GET  -> empty form, OR pre-populated form when ?draft=<id> is provided.
    POST -> validate and either:
              - create a new Message (when not editing a draft), OR
              - update the existing draft Message (when editing).
            The `action` field on the submitted form tells us whether this is
            a Send (action=send) or Save Draft (action=save_draft).

    Covers test cases TC-M1-01..04, TC-M2-01..02, and TC-M5-03 (edit draft).

    Note on the `errors` dict: keys are field names ('recipient', 'subject',
    'body') plus a catch-all key 'form_error'. We avoid Django's '__all__'
    convention because Django's template language disallows variable names
    starting with '_'.
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

    # --- Are we editing an existing draft? ---
    # The ?draft=<id> query parameter triggers edit mode. We look it up
    # carefully: must exist, must be ours, must actually be a draft.
    # Any failure of those checks -> redirect to drafts list with an error.
    editing_draft = None
    draft_id = request.GET.get('draft') or request.POST.get('draft_id')
    if draft_id:
        try:
            editing_draft = Message.objects.get(
                pk=draft_id,
                sender=my_profile,
                is_draft=True,
            )
        except Message.DoesNotExist:
            django_messages.error(request, "Draft not found.")
            return redirect('messages_drafts')

    errors = {}

    # Decide initial form values: pre-populate from draft if editing, else empty.
    if editing_draft and request.method == 'GET':
        form_data = {
            'recipient': str(editing_draft.recipient.pk) if editing_draft.recipient else '',
            'subject': editing_draft.subject,
            'body': editing_draft.body,
        }
    else:
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

        # --- on success, create OR update ---
        if not errors:
            is_draft = (action == 'save_draft')

            if editing_draft:
                # Update the existing draft row in place.
                editing_draft.recipient = recipient
                editing_draft.subject = subject
                editing_draft.body = body
                editing_draft.is_draft = is_draft
                editing_draft.save()  # auto_now field 'updated_at' refreshes here
                if is_draft:
                    django_messages.success(request, 'Draft updated.')
                    return redirect('messages_drafts')
                else:
                    django_messages.success(request, 'Message sent.')
                    return redirect('messages')
            else:
                # Brand new message.
                Message.objects.create(
                    sender=my_profile,
                    recipient=recipient,
                    subject=subject,
                    body=body,
                    is_draft=is_draft,
                )
                if is_draft:
                    django_messages.success(request, 'Draft saved.')
                    return redirect('messages_drafts')
                else:
                    django_messages.success(request, 'Message sent.')
                    return redirect('messages')

    context = {
        'recipients': recipients,
        'errors': errors,
        'form_data': form_data,
        'editing_draft': editing_draft,
    }
    return render(request, 'messages/compose.html', context)

# ---------- UC-M4: View Sent ----------

@login_required
def sent(request):
    """Display all non-draft messages where the current user is the sender.

    Mirrors the inbox view but filters by sender instead of recipient and
    excludes drafts (drafts have their own view in UC-M5).

    select_related('recipient') pre-fetches the recipient profile in one
    SQL query, avoiding the N+1 query problem when rendering the list —
    same optimisation pattern used in inbox().
    """
    my_profile = _get_current_profile(request)

    if my_profile is None:
        messages_list = []
    else:
        messages_list = (
            Message.objects
            .filter(sender=my_profile, is_draft=False)
            .select_related('recipient')
        )

    context = {
        'messages_list': messages_list,
        'has_profile': my_profile is not None,
    }
    return render(request, 'messages/sent.html', context)

# ---------- UC-M5: View Drafts ----------

@login_required
def drafts(request):
    """Display all drafts authored by the current user.

    Drafts are messages with is_draft=True. They live in the same Message
    table as sent messages but are filtered out of inbox/sent views and
    surfaced here. Each draft is editable (-> compose with ?draft=<id>)
    and deletable (-> delete_draft view).

    select_related('recipient') pre-fetches the recipient profile in one
    SQL query. A draft may have no recipient yet (recipient is nullable),
    in which case the partial template handles the None case explicitly.
    """
    my_profile = _get_current_profile(request)

    if my_profile is None:
        messages_list = []
    else:
        messages_list = (
            Message.objects
            .filter(sender=my_profile, is_draft=True)
            .select_related('recipient')
        )

    context = {
        'messages_list': messages_list,
        'has_profile': my_profile is not None,
    }
    return render(request, 'messages/drafts.html', context)

@login_required
def delete_draft(request, pk):
    """Delete a draft. Restricted to POST and to the draft's owner.

    POST-only because deletes shouldn't happen via GET — that would let an
    attacker delete drafts by tricking the user into visiting a URL (or by
    a browser pre-fetching the link). POST requires a form submission with
    a valid CSRF token, mitigating both attacks.

    The lookup also verifies sender=request.user.profile and is_draft=True;
    a missing-or-not-yours-or-not-a-draft row 404s rather than leaking which
    of those was wrong.
    """
    if request.method != 'POST':
        # Reject non-POST requests with a 405 Method Not Allowed.
        from django.http import HttpResponseNotAllowed
        return HttpResponseNotAllowed(['POST'])

    my_profile = _get_current_profile(request)
    if my_profile is None:
        django_messages.warning(request, "Your account has no Profile yet.")
        return redirect('messages_drafts')

    try:
        draft = Message.objects.get(pk=pk, sender=my_profile, is_draft=True)
    except Message.DoesNotExist:
        django_messages.error(request, "Draft not found.")
        return redirect('messages_drafts')

    draft.delete()
    django_messages.success(request, 'Draft deleted.')
    return redirect('messages_drafts')