from django.db.models import Q
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

    query = request.GET.get('q', '').strip()

    employees = Profile.objects.select_related(
        'user', 'team', 'department', 'manager'
    )

    if query:
        employees = employees.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(user__email__icontains=query)
            | Q(team__team_name__icontains=query)
            | Q(department__department_name__icontains=query)
        )

    employees = employees.order_by('first_name', 'last_name')

    context = {
        'total_departments': total_departments,
        'total_teams': total_teams,
        'on_track_teams': on_track_teams,
        'at_risk_teams': at_risk_teams,
        'blocked_teams': blocked_teams,
        'upcoming_meetings': upcoming_meetings,
        'employees': employees,
        'query': query,
    }

    return render(request, 'dashboard/index.html', context)