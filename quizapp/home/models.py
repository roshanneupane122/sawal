from django.db import models

# Create your models here.
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    option1 = models.CharField(max_length=50)
    option2 = models.CharField(max_length=50)
    option3 = models.CharField(max_length=50)
    option4 = models.CharField(max_length=50)
    correct_option = models.CharField(max_length=50)

from django.db import models
from django.contrib.auth.models import User

class QuizSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    final_score = models.IntegerField()
   

