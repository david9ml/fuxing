from django.contrib import admin
from intemass.question.models import Question,StandardAnswer,QuestionImage

admin.site.register(Question)
admin.site.register(StandardAnswer)
admin.site.register(QuestionImage)
