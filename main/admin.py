from django.contrib import admin
from .models import Profile
from .models import Department
from .models import Team
from .models import Meeting
# Register your models here.

admin.site.register(Profile)
admin.site.register(Department)
admin.site.register(Team)
admin.site.register(Meeting)
