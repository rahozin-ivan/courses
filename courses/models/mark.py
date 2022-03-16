from django.db import models
from django.core.validators import MinValueValidator

from courses.models import HomeworkAnswer


class Mark(models.Model):
    homework_answer = models.OneToOneField(HomeworkAnswer, on_delete=models.CASCADE, related_name='mark')
    mark = models.IntegerField('Mark', validators=[MinValueValidator(0), ], default=0)
