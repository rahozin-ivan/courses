from django.db import models
from django.contrib.auth import get_user_model

from courses.models import Mark


class Comment(models.Model):
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
