from django.contrib import admin
from .models import Profile
from .models import Department
from .models import Team
# Register your models here.

admin.site.register(Profile)
admin.site.register(Department)
admin.site.register(Team)
