from django.contrib import admin
from .models import Profile
from .models import Department
from .models import Team
from .models import Meeting
from .models import Message   # added by Kirtan (Messages module)
# Register your models here.

admin.site.register(Profile)
admin.site.register(Department)
admin.site.register(Team)
admin.site.register(Meeting)
admin.site.register(Message)   # added by Kirtan (Messages module)
