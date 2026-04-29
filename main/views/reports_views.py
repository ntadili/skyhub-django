# Created by Batuhan Amirzehni

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from main.models import Team, Department, Profile
import csv


@login_required
def reports(request):
    teams = Team.objects.select_related("department_name", "team_leader").all()
    departments = Department.objects.all()

    total_teams = teams.count()
    total_departments = departments.count()

    teams_without_leaders = teams.filter(team_leader__isnull=True)

    on_track_teams = teams.filter(status="on_track").count()
    at_risk_teams = teams.filter(status="at_risk").count()
    blocked_teams = teams.filter(status="blocked").count()

    department_summary = []
    for department in departments:
        department_teams = teams.filter(department_name=department)

        department_summary.append({
            "department": department,
            "team_count": department_teams.count(),
            "member_count": Profile.objects.filter(department=department).count(),
        })

    context = {
        "total_teams": total_teams,
        "total_departments": total_departments,
        "teams_without_leaders": teams_without_leaders,
        "teams_without_leaders_count": teams_without_leaders.count(),
        "on_track_teams": on_track_teams,
        "at_risk_teams": at_risk_teams,
        "blocked_teams": blocked_teams,
        "department_summary": department_summary,
    }

    return render(request, "reports/reports.html", context)


@login_required
def export_reports_csv(request):
    teams = Team.objects.select_related("department_name", "team_leader").all()

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="skyhub_team_report.csv"'

    writer = csv.writer(response)
    writer.writerow(["Team Name", "Department", "Team Leader", "Status", "Mission"])

    for team in teams:
        writer.writerow([
            team.team_name,
            team.department_name.department_name if team.department_name else "No Department",
            team.leader_name if team.leader_name else "No Leader",
            team.get_status_display(),
            team.mission,
        ])

    return response