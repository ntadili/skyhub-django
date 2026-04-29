from django.shortcuts import render, get_object_or_404
from main.models import Team, Department

def team_list(request):
    teams = Team.objects.select_related('department_name', 'team_leader__profile').prefetch_related('members')
    departments = Department.objects.all()

    dept_filter = request.GET.get('department', '')
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('q', '')

    if dept_filter:
        teams = teams.filter(department_name__id=dept_filter)
    if status_filter:
        teams = teams.filter(status=status_filter)
    if search_query:
        teams = teams.filter(team_name__icontains=search_query)

    return render(request, 'teams/teams.html', {
        'teams': teams,
        'departments': departments,
        'dept_filter': dept_filter,
        'status_filter': status_filter,
        'search_query': search_query,
    })

def team_detail(request, team_id):
    team = get_object_or_404(
        Team.objects.select_related('department_name', 'team_leader__profile').prefetch_related('members__user'),
        id=team_id
    )
    return render(request, 'teams/team_detail.html', {'team': team})