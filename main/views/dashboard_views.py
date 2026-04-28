from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from main.models import Department, Team, Meeting, Profile


HEADCOUNT_MONTHS = 6

DEPARTMENT_PALETTE = [
    '#2563eb',  # blue
    '#10b981',  # green
    '#f59e0b',  # amber
    '#ec4899',  # pink
    '#8b5cf6',  # purple
    '#06b6d4',  # cyan
]


def _month_buckets(months):
    """Return a list of (start, end_exclusive) datetimes for the last N months,
    oldest first. `end_exclusive` is the first day of the following month."""
    now = timezone.now()
    cursor = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    buckets = []
    for _ in range(months):
        if cursor.month == 12:
            nxt = cursor.replace(year=cursor.year + 1, month=1)
        else:
            nxt = cursor.replace(month=cursor.month + 1)
        buckets.append((cursor, nxt))

        if cursor.month == 1:
            cursor = cursor.replace(year=cursor.year - 1, month=12)
        else:
            cursor = cursor.replace(month=cursor.month - 1)

    buckets.reverse()
    return buckets


def _department_headcount_series(months=HEADCOUNT_MONTHS):
    """Cumulative headcount per department across the last N months."""
    buckets = _month_buckets(months)
    labels = [start.strftime('%b %Y') for start, _ in buckets]

    series = []
    for i, dept in enumerate(Department.objects.order_by('department_name')):
        data = []
        for _start, end in buckets:
            count = Profile.objects.filter(
                department=dept,
                created_at__lt=end,
            ).count()
            data.append(count)
        series.append({
            'label': dept.department_name,
            'data': data,
            'color': DEPARTMENT_PALETTE[i % len(DEPARTMENT_PALETTE)],
        })

    return labels, series

@login_required
def dashboard(request):
    total_departments = Department.objects.count()
    total_teams = Team.objects.count()
    total_employees = Profile.objects.count()

    on_track_teams = Team.objects.filter(status='on_track').count()
    at_risk_teams = Team.objects.filter(status='at_risk').count()
    blocked_teams = Team.objects.filter(status='blocked').count()

    headcount_labels, headcount_series = _department_headcount_series()

    upcoming_meetings = (
        Meeting.objects
        .filter(date_time__gte=timezone.now())
        .prefetch_related('participants')
        .order_by('date_time')[:1]
    )

    query = request.GET.get('q', '').strip()

    employees = Profile.objects.select_related(
        'user', 'team__team_leader__profile', 'department'
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
        'total_employees': total_employees,
        'on_track_teams': on_track_teams,
        'at_risk_teams': at_risk_teams,
        'blocked_teams': blocked_teams,
        'headcount_labels': headcount_labels,
        'headcount_series': headcount_series,
        'upcoming_meetings': upcoming_meetings,
        'employees': employees,
        'query': query,
    }

    return render(request, 'dashboard/index.html', context)