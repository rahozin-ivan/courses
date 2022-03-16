from django.db import models


class CourseManager(models.Manager):
    def user_courses(self, user):
        return super().filter(models.Q(teachers=user) | models.Q(students=user)).distinct()
