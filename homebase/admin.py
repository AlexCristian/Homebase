from django.contrib import admin

from .models import User, Course, Assignment, Meeting
# Register your models here.

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Meeting)
