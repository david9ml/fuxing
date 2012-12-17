from django.contrib import admin
from intemass.student.models import StudentAnswer

class StudentAnswerAdmin(admin.ModelAdmin):
	list_display = ('student', 'question', 'mark')

admin.site.register(StudentAnswer, StudentAnswerAdmin)
