from django.contrib import admin
from intemass.classroom.models import Classroom

class ClassAdmin(admin.ModelAdmin):
	list_display = ('roomname', 'volume', 'date_created')

admin.site.register(Classroom, ClassAdmin)
