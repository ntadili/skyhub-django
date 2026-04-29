"""
Account-related views (registration).

Login / logout / password-change all use Django's built-in class-based
views, wired up directly in main/urls/login_urls.py. Only registration
needs a custom view because we have to create the linked Profile too.
"""

from django import forms
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from main.models import Profile


class SkyHubRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


def register(request):
    """Self-registration. Creates a User + linked Profile, then logs the user in."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SkyHubRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            Profile.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )

            login(request, user)
            return redirect('dashboard')
    else:
        form = SkyHubRegisterForm()

    return render(request, 'login/register.html', {'form': form})
