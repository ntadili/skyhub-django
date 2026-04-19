from django.shortcuts import render

def schedule_page(request):
    return render(request, 'schedule/schedule.html')