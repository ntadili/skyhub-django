# Created by Batuhan Amirzehni

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from main.models import Department, Team, Profile


@login_required
def organisation_page(request):
    selected_status = request.GET.get("status", "all")
    selected_sort = request.GET.get("sort", "department_name")

    departments = Department.objects.select_related("department_leader").all()
    teams = Team.objects.select_related("department_name", "team_leader").all()

    if selected_status != "all":
        teams = teams.filter(status=selected_status)

    total_departments = departments.count()
    total_teams = Team.objects.count()
    total_members = Profile.objects.count()
    teams_without_leaders = Team.objects.filter(team_leader__isnull=True).count()

    on_track_teams = Team.objects.filter(status="on_track").count()
    at_risk_teams = Team.objects.filter(status="at_risk").count()
    blocked_teams = Team.objects.filter(status="blocked").count()

    department_data = []

    for department in departments:
        department_teams = teams.filter(department_name=department)
        all_department_teams = Team.objects.filter(department_name=department)
        department_members = Profile.objects.filter(department=department)

        blocked_count = all_department_teams.filter(status="blocked").count()
        at_risk_count = all_department_teams.filter(status="at_risk").count()

        department_data.append({
            "department": department,
            "teams": department_teams,
            "team_count": all_department_teams.count(),
            "filtered_team_count": department_teams.count(),
            "member_count": department_members.count(),
            "blocked_count": blocked_count,
            "at_risk_count": at_risk_count,
            "risk_score": blocked_count * 2 + at_risk_count,
        })

    if selected_sort == "team_count":
        department_data.sort(key=lambda item: item["team_count"], reverse=True)
    elif selected_sort == "risk":
        department_data.sort(key=lambda item: item["risk_score"], reverse=True)
    else:
        department_data.sort(key=lambda item: item["department"].department_name)

    context = {
        "department_data": department_data,
        "total_departments": total_departments,
        "total_teams": total_teams,
        "total_members": total_members,
        "teams_without_leaders": teams_without_leaders,
        "on_track_teams": on_track_teams,
        "at_risk_teams": at_risk_teams,
        "blocked_teams": blocked_teams,
        "selected_status": selected_status,
        "selected_sort": selected_sort,
    }

    return render(request, "organisation/organisation.html", context)