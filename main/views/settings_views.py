"""Settings page — currently hosts the change-password form."""

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render


@login_required
def settings_index(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keep the user logged in after the password rotates.
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully.')
            return redirect('settings')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'settings/settings.html', {'form': form})
