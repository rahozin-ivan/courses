from django.db import models
from django.contrib.auth import get_user_model

from .course import Course


class Lecture(models.Model):
    name = models.CharField('Lecture name', max_length=50)
    presentation = models.FileField('Presentation', upload_to='lectures/')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='lectures')

    def __str__(self):
        return self.name
