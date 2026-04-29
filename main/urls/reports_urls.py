# Created by Batuhan Amirzehni

from django.urls import path
from main.views import reports_views

urlpatterns = [
    path("", reports_views.reports, name="reports"),
    path("export/csv/", reports_views.export_reports_csv, name="export_reports_csv"),
]