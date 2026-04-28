from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def organisation_page(request):
    return render(request, 'organisation/organisation.html')
