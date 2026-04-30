from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from main.models import Department, Team, Meeting, Profile


# Headcount chart window: last 40 days, sampled every 5 days.
HEADCOUNT_DAYS = 40
HEADCOUNT_STEP_DAYS = 5

DEPARTMENT_PALETTE = [
    '#2563eb',  # blue
    '#10b981',  # green
    '#f59e0b',  # amber
    '#ec4899',  # pink
    '#8b5cf6',  # purple
    '#06b6d4',  # cyan
]


def _week_buckets(days=HEADCOUNT_DAYS, step=HEADCOUNT_STEP_DAYS):
    """Return a list of (start, end_exclusive) datetimes covering the last
    `days` days, stepped every `step` days, oldest first."""
    now = timezone.now()
    end_today = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    start_window = end_today - timedelta(days=days)

    buckets = []
    cursor = start_window
    while cursor < end_today:
        nxt = min(cursor + timedelta(days=step), end_today)
        buckets.append((cursor, nxt))
        cursor = nxt
    return buckets


def _department_headcount_series(days=HEADCOUNT_DAYS, step=HEADCOUNT_STEP_DAYS):
    """Cumulative headcount per department, sampled at the end of each
    weekly bucket across the last `days` days."""
    buckets = _week_buckets(days, step)
    labels = [end.strftime('%-d %b') for _start, end in buckets]

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

    # Health-bar percentages (avoid divide-by-zero)
    if total_teams:
        clear_pct = round(on_track_teams / total_teams * 100)
        risk_pct = round(at_risk_teams / total_teams * 100)
        blocked_pct = max(0, 100 - clear_pct - risk_pct)
    else:
        clear_pct = risk_pct = blocked_pct = 0

    # "Joined this month" delta for the headline KPI
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    new_employees_this_month = Profile.objects.filter(
        created_at__gte=start_of_month
    ).count()

    headcount_labels, headcount_series = _department_headcount_series()

    upcoming_meetings = (
        Meeting.objects
        .filter(date_time__gte=timezone.now())
        .prefetch_related('participants')
        .order_by('date_time')[:4]
    )

    query = request.GET.get('q', '').strip()
    filter_team = request.GET.get('team', '').strip()
    filter_department = request.GET.get('department', '').strip()
    filter_manager = request.GET.get('manager', '').strip()

    employees = Profile.objects.select_related(
        'user', 'team__team_leader__profile', 'department'
    )

    if query:
        employees = employees.filter(
            # Employee name (first / last)
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            # Email
            | Q(user__email__icontains=query)
            # Team name
            | Q(team__team_name__icontains=query)
            # Department name
            | Q(department__department_name__icontains=query)
            # Manager (team leader) — match their Profile name or username
            | Q(team__team_leader__profile__first_name__icontains=query)
            | Q(team__team_leader__profile__last_name__icontains=query)
            | Q(team__team_leader__username__icontains=query)
        ).distinct()

    # Apply explicit filter (one at a time)
    active_filter = None
    if filter_team:
        team_obj = Team.objects.filter(pk=filter_team).first()
        if team_obj:
            employees = employees.filter(team=team_obj)
            active_filter = {'type': 'team', 'label': 'Team', 'value': team_obj.team_name, 'id': team_obj.pk}
    elif filter_department:
        dept_obj = Department.objects.filter(pk=filter_department).first()
        if dept_obj:
            employees = employees.filter(department=dept_obj)
            active_filter = {'type': 'department', 'label': 'Department', 'value': dept_obj.department_name, 'id': dept_obj.pk}
    elif filter_manager:
        mgr_obj = User.objects.filter(pk=filter_manager).first()
        if mgr_obj:
            employees = employees.filter(team__team_leader=mgr_obj)
            try:
                mgr_label = f"{mgr_obj.profile.first_name} {mgr_obj.profile.last_name}".strip() or mgr_obj.username
            except Profile.DoesNotExist:
                mgr_label = mgr_obj.username
            active_filter = {'type': 'manager', 'label': 'Manager', 'value': mgr_label, 'id': mgr_obj.pk}

    employees = employees.order_by('first_name', 'last_name')

    # Filter dropdown option lists
    filter_teams = Team.objects.order_by('team_name')
    filter_departments = Department.objects.order_by('department_name')
    manager_user_ids = (
        Team.objects.filter(team_leader__isnull=False)
        .values_list('team_leader_id', flat=True)
        .distinct()
    )
    filter_managers = list(
        User.objects.filter(id__in=manager_user_ids).select_related('profile')
    )

    def _manager_display(user):
        try:
            full = f"{user.profile.first_name} {user.profile.last_name}".strip()
            return full or user.username
        except Profile.DoesNotExist:
            return user.username

    filter_managers_options = sorted(
        ({'id': u.id, 'label': _manager_display(u)} for u in filter_managers),
        key=lambda m: m['label'].lower(),
    )

    context = {
        'total_departments': total_departments,
        'total_teams': total_teams,
        'total_employees': total_employees,
        'new_employees_this_month': new_employees_this_month,
        'on_track_teams': on_track_teams,
        'at_risk_teams': at_risk_teams,
        'blocked_teams': blocked_teams,
        'clear_pct': clear_pct,
        'risk_pct': risk_pct,
        'blocked_pct': blocked_pct,
        'headcount_labels': headcount_labels,
        'headcount_series': headcount_series,
        'upcoming_meetings': upcoming_meetings,
        'employees': employees,
        'query': query,
        'filter_teams': filter_teams,
        'filter_departments': filter_departments,
        'filter_managers': filter_managers_options,
        'active_filter': active_filter,
    }

    return render(request, 'dashboard/index.html', context)