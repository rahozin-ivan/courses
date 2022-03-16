from django.db import models
from django.contrib.auth import get_user_model

from courses.models import Homework


class HomeworkAnswer(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='answers')
    answer = models.TextField('Answer')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='homework_answers')
