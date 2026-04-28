"""
URL configuration for skyhub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('main.urls.dashboard_urls')),
    path('login/', include('main.urls.login_urls')),
    path('teams/', include('main.urls.teams_urls')),
    path('organisation/', include('main.urls.organisation_urls')),
    path('messages/', include('main.urls.messages_urls')),
    path('schedule/', include('main.urls.schedule_urls')),
    
    # REPORTS MODULE - BATUHAN AMIRZEHNI
    path('reports/', include('main.urls.reports_urls')),
]



