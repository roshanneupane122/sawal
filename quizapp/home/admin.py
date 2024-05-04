
from django.contrib import admin
from .models import Question,QuizSession

admin.site.register(Question)
# Register your models here.
admin.site.register(QuizSession)
