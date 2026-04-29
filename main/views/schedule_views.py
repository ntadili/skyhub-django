from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def schedule_page(request):
    return render(request, 'schedule/schedule.html')
