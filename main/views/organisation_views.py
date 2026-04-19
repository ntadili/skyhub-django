from django.shortcuts import render

def organisation_page(request):
    return render(request, 'organisation/organisation.html')