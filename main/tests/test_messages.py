"""
Tests for the Messages module (Kirtan Sodha, Student 3 — UC-M1 to UC-M6).

Each UC has its own TestCase subclass below. Test method names encode the
TC IDs from the CW1 group test plan (e.g. test_tc_m1_01_send_valid_message)
so the test runner output traces back directly to each documented case.

Run the full suite:
    python manage.py test main.tests.test_messages
"""

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User

from main.models import Profile, Message


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class MessagesTestBase(TestCase):
    """Shared fixtures and helpers for every Messages module test class."""

    @classmethod
    def setUpTestData(cls):
        cls.user_kirtan = User.objects.create_user(
            username='kirtan',
            password='testpass123',
        )
        cls.profile_kirtan = Profile.objects.create(
            user=cls.user_kirtan,
            first_name='Kirtan',
            last_name='Sodha',
        )

        cls.user_alex = User.objects.create_user(
            username='alex',
            password='testpass123',
        )
        cls.profile_alex = Profile.objects.create(
            user=cls.user_alex,
            first_name='Alex',
            last_name='Thompson',
        )

        cls.user_intruder = User.objects.create_user(
            username='intruder',
            password='testpass123',
        )
        cls.profile_intruder = Profile.objects.create(
            user=cls.user_intruder,
            first_name='Mal',
            last_name='Lory',
        )

    def login_as_kirtan(self):
        self.client.force_login(self.user_kirtan)

    def login_as_alex(self):
        self.client.force_login(self.user_alex)

    def login_as_intruder(self):
        self.client.force_login(self.user_intruder)


class FixtureSmokeTests(MessagesTestBase):
    """Sanity checks that MessagesTestBase produces the expected fixtures."""

    def test_three_users_and_profiles_created(self):
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(Profile.objects.count(), 3)
        self.assertEqual(self.user_kirtan.profile, self.profile_kirtan)
        self.assertEqual(self.profile_kirtan.first_name, 'Kirtan')

    def test_login_helper_authenticates_client(self):
        self.assertNotIn('_auth_user_id', self.client.session)
        self.login_as_kirtan()
        self.assertEqual(
            int(self.client.session['_auth_user_id']),
            self.user_kirtan.pk,
        )


# ===========================================================================
# UC-M1: Send Message
# ===========================================================================

class UCM1SendMessageTests(MessagesTestBase):
    """TC-M1-01..04: UC-M1 Send Message."""

    def test_tc_m1_01_send_valid_message(self):
        """TC-M1-01 (Positive): logged-in user with valid recipient, subject
        and body successfully sends; row appears in DB and view redirects
        to inbox."""
        self.login_as_kirtan()

        response = self.client.post(reverse('messages_compose'), {
            'recipient': self.profile_alex.pk,
            'subject': 'Project Update',
            'body': 'Draft completed.',
            'action': 'send',
        })

        self.assertRedirects(response, reverse('messages'))
        self.assertEqual(Message.objects.count(), 1)
        msg = Message.objects.first()
        self.assertEqual(msg.sender, self.profile_kirtan)
        self.assertEqual(msg.recipient, self.profile_alex)
        self.assertEqual(msg.subject, 'Project Update')
        self.assertEqual(msg.body, 'Draft completed.')
        self.assertFalse(msg.is_draft)

    def test_tc_m1_02_send_blocked_when_recipient_missing(self):
        """TC-M1-02 (Negative): clicking Send with no recipient re-renders
        the form with a 'Recipient is required' error; no row created."""
        self.login_as_kirtan()

        response = self.client.post(reverse('messages_compose'), {
            'recipient': '',
            'subject': 'Test',
            'body': 'Hello',
            'action': 'send',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('recipient', response.context['errors'])
        self.assertEqual(
            response.context['errors']['recipient'],
            'Recipient is required.',
        )
        self.assertEqual(Message.objects.count(), 0)

    def test_tc_m1_03_redirects_anonymous_user_to_login(self):
        """TC-M1-03 (Negative): unauthenticated request to compose is
        redirected to login with ?next= so the user lands back here
        after authenticating."""
        response = self.client.get(reverse('messages_compose'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
        self.assertIn('next=/messages/compose/', response.url)

    def test_tc_m1_04_send_with_max_length_subject(self):
        """TC-M1-04 (Edge): a 255-character subject (the field's max_length)
        sends successfully without truncation."""
        self.login_as_kirtan()

        long_subject = 'a' * 255
        response = self.client.post(reverse('messages_compose'), {
            'recipient': self.profile_alex.pk,
            'subject': long_subject,
            'body': 'Test',
            'action': 'send',
        })

        self.assertRedirects(response, reverse('messages'))
        self.assertEqual(Message.objects.count(), 1)
        msg = Message.objects.first()
        self.assertEqual(len(msg.subject), 255)
        self.assertEqual(msg.subject, long_subject)


# ===========================================================================
# UC-M2: Save Draft
# ===========================================================================

class UCM2SaveDraftTests(MessagesTestBase):
    """TC-M2-01..04: UC-M2 Save Draft."""

    def test_tc_m2_01_save_draft_with_subject_and_body(self):
        """TC-M2-01 (Positive): clicking Save Draft persists a Message with
        is_draft=True and redirects to the Drafts list."""
        self.login_as_kirtan()

        response = self.client.post(reverse('messages_compose'), {
            'recipient': '',
            'subject': 'Project Update',
            'body': 'Work in progress...',
            'action': 'save_draft',
        })

        self.assertRedirects(response, reverse('messages_drafts'))
        self.assertEqual(Message.objects.count(), 1)
        msg = Message.objects.first()
        self.assertEqual(msg.sender, self.profile_kirtan)
        self.assertIsNone(msg.recipient)
        self.assertEqual(msg.subject, 'Project Update')
        self.assertEqual(msg.body, 'Work in progress...')
        self.assertTrue(msg.is_draft)

    def test_tc_m2_02_save_draft_with_blank_subject(self):
        """TC-M2-02 (Edge): a draft with blank subject but non-empty body
        is still saved (subject is optional for drafts)."""
        self.login_as_kirtan()

        response = self.client.post(reverse('messages_compose'), {
            'recipient': '',
            'subject': '',
            'body': 'Some text',
            'action': 'save_draft',
        })

        self.assertRedirects(response, reverse('messages_drafts'))
        self.assertEqual(Message.objects.count(), 1)
        msg = Message.objects.first()
        self.assertEqual(msg.subject, '')
        self.assertEqual(msg.body, 'Some text')
        self.assertTrue(msg.is_draft)

    def test_tc_m2_03_edit_existing_draft_updates_in_place(self):
        """TC-M2-03 (Positive): editing a draft updates the existing row
        rather than creating a new one. Pk preserved; subject/body changed."""
        self.login_as_kirtan()

        draft = Message.objects.create(
            sender=self.profile_kirtan,
            subject='Project Update',
            body='Original body',
            is_draft=True,
        )

        response = self.client.post(reverse('messages_compose'), {
            'draft_id': draft.pk,
            'recipient': '',
            'subject': 'Quarterly Update',
            'body': 'Updated content',
            'action': 'save_draft',
        })

        self.assertRedirects(response, reverse('messages_drafts'))
        self.assertEqual(Message.objects.count(), 1)
        draft.refresh_from_db()
        self.assertEqual(draft.subject, 'Quarterly Update')
        self.assertEqual(draft.body, 'Updated content')
        self.assertTrue(draft.is_draft)

    def test_tc_m2_04_drafts_redirects_anonymous_user_to_login(self):
        """TC-M2-04 (Negative): unauthenticated request to Drafts redirects
        to login."""
        response = self.client.get(reverse('messages_drafts'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
        self.assertIn('next=/messages/drafts/', response.url)


# ===========================================================================
# UC-M3: View Inbox
# ===========================================================================

class UCM3InboxTests(MessagesTestBase):
    """TC-M3-01..04: UC-M3 View Inbox."""

    def test_tc_m3_01_inbox_lists_received_messages(self):
        """TC-M3-01 (Positive): inbox shows non-draft messages where the
        current user is the recipient. Sender's own sent messages and
        other users' messages do not appear."""
        self.login_as_kirtan()

        for_kirtan = Message.objects.create(
            sender=self.profile_alex,
            recipient=self.profile_kirtan,
            subject='Hello Kirtan',
            body='Test',
        )
        Message.objects.create(
            sender=self.profile_kirtan,
            recipient=self.profile_alex,
            subject='Reply',
            body='Test',
        )
        Message.objects.create(
            sender=self.profile_alex,
            recipient=self.profile_intruder,
            subject='Other',
            body='Test',
        )

        response = self.client.get(reverse('messages'))

        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages_list'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0], for_kirtan)

    def test_tc_m3_02_empty_inbox_renders_empty_state(self):
        """TC-M3-02 (Edge): with no messages in DB, inbox renders without
        crashing; messages_list is empty."""
        self.login_as_kirtan()

        response = self.client.get(reverse('messages'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(list(response.context['messages_list'])), 0)
        self.assertEqual(response.context['unread_count'], 0)

    def test_tc_m3_03_drafts_excluded_from_inbox(self):
        """TC-M3-03 (Edge): drafts (is_draft=True) never appear in inbox,
        even if they have a recipient set."""
        self.login_as_kirtan()

        Message.objects.create(
            sender=self.profile_alex,
            recipient=self.profile_kirtan,
            subject='Draft to kirtan',
            body='Draft body',
            is_draft=True,
        )
        real = Message.objects.create(
            sender=self.profile_alex,
            recipient=self.profile_kirtan,
            subject='Real message',
            body='Real body',
        )

        response = self.client.get(reverse('messages'))

        messages_list = list(response.context['messages_list'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0], real)

    def test_tc_m3_04_inbox_redirects_anonymous_user_to_login(self):
        """TC-M3-04 (Negative): unauthenticated GET on inbox redirects
        to login with ?next= preserving the original URL."""
        response = self.client.get(reverse('messages'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
        self.assertIn('next=/messages/', response.url)


# ===========================================================================
# UC-M4: View Sent
# ===========================================================================

class UCM4SentTests(MessagesTestBase):
    """TC-M4-01..04: UC-M4 View Sent."""

    def test_tc_m4_01_sent_lists_sent_messages(self):
        """TC-M4-01 (Positive): sent view shows non-draft messages where
        the current user is the sender."""
        self.login_as_kirtan()

        from_kirtan = Message.objects.create(
            sender=self.profile_kirtan,
            recipient=self.profile_alex,
            subject='From kirtan',
            body='Test',
        )
        Message.objects.create(
            sender=self.profile_alex,
            recipient=self.profile_kirtan,
            subject='To kirtan',
            body='Test',
        )

        response = self.client.get(reverse('messages_sent'))

        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages_list'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0], from_kirtan)

    def test_tc_m4_02_empty_sent_renders_empty_state(self):
        """TC-M4-02 (Edge): with no sent messages, view renders cleanly
        with an empty list."""
        self.login_as_kirtan()

        response = self.client.get(reverse('messages_sent'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(list(response.context['messages_list'])), 0)

    def test_tc_m4_03_drafts_excluded_from_sent(self):
        """TC-M4-03 (Edge): drafts authored by the current user do not
        leak into Sent — they belong only in Drafts."""
        self.login_as_kirtan()

        Message.objects.create(
            sender=self.profile_kirtan,
            recipient=self.profile_alex,
            subject='Draft',
            body='Draft body',
            is_draft=True,
        )
        sent_msg = Message.objects.create(
            sender=self.profile_kirtan,
            recipient=self.profile_alex,
            subject='Sent',
            body='Real body',
        )

        response = self.client.get(reverse('messages_sent'))

        messages_list = list(response.context['messages_list'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0], sent_msg)

    def test_tc_m4_04_sent_redirects_anonymous_user_to_login(self):
        """TC-M4-04 (Negative): unauthenticated GET on Sent redirects
        to login."""
        response = self.client.get(reverse('messages_sent'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
        self.assertIn('next=/messages/sent/', response.url)


# ===========================================================================
# UC-M5: View Drafts (list + edit + delete)
# ===========================================================================

class UCM5DraftsTests(MessagesTestBase):
    """TC-M5-01..05: UC-M5 View Drafts."""

    def test_tc_m5_01_drafts_lists_user_drafts(self):
        """TC-M5-01 (Positive): drafts page lists the current user's
        drafts; sent messages and other users' drafts do not appear."""
        self.login_as_kirtan()

        my_draft = Message.objects.create(
            sender=self.profile_kirtan,
            subject='My Draft',
            body='Draft body',
            is_draft=True,
        )
        Message.objects.create(
            sender=self.profile_kirtan,
            recipient=self.profile_alex,
            subject='Sent message',
            body='Sent body',
        )
        Message.objects.create(
            sender=self.profile_alex,
            subject="Alex's draft",
            body='Other body',
            is_draft=True,
        )

        response = self.client.get(reverse('messages_drafts'))

        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages_list'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0], my_draft)

    def test_tc_m5_02_empty_drafts_renders_empty_state(self):
        """TC-M5-02 (Edge): with no drafts, the page renders cleanly with
        an empty list."""
        self.login_as_kirtan()

        response = self.client.get(reverse('messages_drafts'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(list(response.context['messages_list'])), 0)

    def test_tc_m5_03_edit_draft_via_query_string_prepopulates_form(self):
        """TC-M5-03 (Positive): GET /messages/compose/?draft=<id> opens
        the compose form with the draft's existing values pre-populated.
        Saving updates the same row, doesn't create a new one."""
        self.login_as_kirtan()

        draft = Message.objects.create(
            sender=self.profile_kirtan,
            recipient=self.profile_alex,
            subject='Original subject',
            body='Original body',
            is_draft=True,
        )

        # GET with ?draft=<id> -> form should be pre-populated.
        response = self.client.get(
            reverse('messages_compose') + f'?draft={draft.pk}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['editing_draft'], draft)
        self.assertEqual(
            response.context['form_data']['subject'],
            'Original subject',
        )
        self.assertEqual(
            response.context['form_data']['body'],
            'Original body',
        )

        # POST update -> same row mutated, no new row.
        response = self.client.post(reverse('messages_compose'), {
            'draft_id': draft.pk,
            'recipient': self.profile_alex.pk,
            'subject': 'Updated subject',
            'body': 'Updated body',
            'action': 'save_draft',
        })
        self.assertRedirects(response, reverse('messages_drafts'))
        self.assertEqual(Message.objects.count(), 1)
        draft.refresh_from_db()
        self.assertEqual(draft.subject, 'Updated subject')
        self.assertEqual(draft.body, 'Updated body')

    def test_tc_m5_04_delete_draft_removes_row_and_redirects(self):
        """TC-M5-04 (Positive): POSTing to delete-draft removes the row
        and redirects back to Drafts. Also covers the IDOR negative case:
        an intruder cannot delete someone else's draft."""
        self.login_as_kirtan()

        draft = Message.objects.create(
            sender=self.profile_kirtan,
            subject='Old Draft',
            body='Old body',
            is_draft=True,
        )

        response = self.client.post(
            reverse('messages_delete_draft', args=[draft.pk])
        )

        self.assertRedirects(response, reverse('messages_drafts'))
        self.assertEqual(Message.objects.count(), 0)

        # IDOR check: re-create the draft, log in as a different user,
        # confirm they can't delete it.
        draft = Message.objects.create(
            sender=self.profile_kirtan,
            subject='Old Draft',
            body='Old body',
            is_draft=True,
        )
        self.client.logout()
        self.login_as_intruder()
        response = self.client.post(
            reverse('messages_delete_draft', args=[draft.pk])
        )
        self.assertRedirects(response, reverse('messages_drafts'))
        # Draft still exists — the intruder's delete was a no-op.
        self.assertEqual(Message.objects.count(), 1)

    def test_tc_m5_05_drafts_redirects_anonymous_user_to_login(self):
        """TC-M5-05 (Negative): unauthenticated GET on Drafts redirects
        to login."""
        response = self.client.get(reverse('messages_drafts'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
        self.assertIn('next=/messages/drafts/', response.url)


# ===========================================================================
# UC-M6: Read Message
# ===========================================================================

class UCM6ReadMessageTests(MessagesTestBase):
    """TC-M6-01..04: UC-M6 Read Message."""

    def test_tc_m6_01_recipient_open_flips_unread_to_read(self):
        """TC-M6-01 (Positive): when the recipient opens an unread
        message, status flips to 'read'. Subject/body/sender all render."""
        self.login_as_kirtan()

        msg = Message.objects.create(
            sender=self.profile_alex,
            recipient=self.profile_kirtan,
            subject='Meeting Notes',
            body='Hello kirtan',
            status='unread',
        )

        response = self.client.get(reverse('messages_read', args=[msg.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['msg'], msg)
        self.assertTrue(response.context['is_recipient'])
        self.assertFalse(response.context['is_sender'])

        # Refresh from DB to confirm the flip persisted.
        msg.refresh_from_db()
        self.assertEqual(msg.status, 'read')

    def test_tc_m6_02_already_read_message_stays_read(self):
        """TC-M6-02 (Positive): re-opening a previously read message
        renders it without changing status."""
        self.login_as_kirtan()

        msg = Message.objects.create(
            sender=self.profile_alex,
            recipient=self.profile_kirtan,
            subject='Already read',
            body='Old message',
            status='read',
        )

        response = self.client.get(reverse('messages_read', args=[msg.pk]))

        self.assertEqual(response.status_code, 200)
        msg.refresh_from_db()
        self.assertEqual(msg.status, 'read')

        # Bonus: when the SENDER opens a message they sent (from Sent view),
        # status must NOT flip even if it were unread.
        unread_sent = Message.objects.create(
            sender=self.profile_kirtan,
            recipient=self.profile_alex,
            subject='From kirtan',
            body='Test',
            status='unread',
        )
        response = self.client.get(
            reverse('messages_read', args=[unread_sent.pk])
        )
        self.assertEqual(response.status_code, 200)
        unread_sent.refresh_from_db()
        self.assertEqual(unread_sent.status, 'unread')

    def test_tc_m6_03_redirects_anonymous_user_to_login(self):
        """TC-M6-03 (Negative): unauthenticated GET on a message URL
        redirects to login. Also covers the IDOR case: an unrelated
        logged-in user cannot view a message they didn't send/receive."""
        msg = Message.objects.create(
            sender=self.profile_alex,
            recipient=self.profile_kirtan,
            subject='Private',
            body='Confidential',
        )

        # Anonymous -> redirect to login.
        response = self.client.get(reverse('messages_read', args=[msg.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

        # Logged-in third party -> 404 (not 403 — don't leak existence).
        self.login_as_intruder()
        response = self.client.get(reverse('messages_read', args=[msg.pk]))
        self.assertEqual(response.status_code, 404)

    def test_tc_m6_04_long_body_renders_without_breaking(self):
        """TC-M6-04 (Edge): a 2000+ character body renders without
        crashing and the full content is in the response."""
        self.login_as_kirtan()

        long_body = 'A long message body. ' * 120  # ~2520 chars
        msg = Message.objects.create(
            sender=self.profile_alex,
            recipient=self.profile_kirtan,
            subject='Long body',
            body=long_body,
        )

        response = self.client.get(reverse('messages_read', args=[msg.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(long_body), 2000)
        # Body content was rendered into the response HTML.
        self.assertContains(response, 'A long message body.')