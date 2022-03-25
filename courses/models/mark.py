from django.db import models
from django.core.validators import MinValueValidator

from courses.models import HomeworkAnswer
from courses.services import send_mark_to_user


class Mark(models.Model):
    homework_answer = models.OneToOneField(HomeworkAnswer, on_delete=models.CASCADE, related_name='mark')
    mark = models.IntegerField('Mark', validators=[MinValueValidator(0), ], default=0)

    def save(self, *args, **kwargs):
        created = self.pk is None

        super().save(*args, **kwargs)

        if created:
            send_mark_to_user(self.homework_answer.user, self.mark)
