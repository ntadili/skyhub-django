from django.shortcuts import render
from django.utils import timezone
from main.models import Department, Team, Meeting, Profile

def dashboard(request):
    total_departments = Department.objects.count()
    total_teams = Team.objects.count()

    on_track_teams = Team.objects.filter(status='on_track').count()
    at_risk_teams = Team.objects.filter(status='at_risk').count()
    blocked_teams = Team.objects.filter(status='blocked').count()

    upcoming_meetings = Meeting.objects.filter(
        date_time__gte=timezone.now()
    ).order_by('date_time')[:5]

    employees = Profile.objects.select_related('user').order_by('first_name', 'last_name')

    context = {
        'total_departments': total_departments,
        'total_teams': total_teams,
        'on_track_teams': on_track_teams,
        'at_risk_teams': at_risk_teams,
        'blocked_teams': blocked_teams,
        'upcoming_meetings': upcoming_meetings,
        'employees': employees,
    }

    return render(request, 'dashboard/index.html', context)