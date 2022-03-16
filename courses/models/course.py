from django.db import models
from django.contrib.auth import get_user_model

from courses.managers import CourseManager


class Course(models.Model):
    name = models.CharField('Course name', max_length=50)
    teachers = models.ManyToManyField(get_user_model(), related_name='courses_as_teacher',
                                      limit_choices_to={'role': get_user_model().RoleChoices.TEACHER})
    students = models.ManyToManyField(get_user_model(), related_name='courses_as_student')
    picture = models.ImageField(null=True, blank=True, upload_to='course_images/')

    objects = CourseManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        created = self.pk is None

        super().save(*args, **kwargs)

        if created:
            from courses.tasks import generate_course_image_based_on_title
            generate_course_image_based_on_title.delay(self.pk)
