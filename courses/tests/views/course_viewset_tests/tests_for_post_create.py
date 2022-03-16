from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from mixer.backend.django import mixer

from courses.models import Course


class CourseViewSetTestsForPostCreateRequest(APITestCase):
    def setUp(self) -> None:
        self.teacher = mixer.blend(get_user_model(), role='Teacher')
        self.student = mixer.blend(get_user_model(), role='Student')
        self.client.force_authenticate(self.teacher)
        self.url = reverse('course-list')

    def test_post_create_not_working_without_login(self):
        self.client.logout()
        res = self.client.post(self.url)
        assert status.HTTP_401_UNAUTHORIZED == res.status_code

    def test_post_create_not_working_for_students(self):
        self.client.force_authenticate(self.student)
        res = self.client.post(self.url)
        assert status.HTTP_403_FORBIDDEN == res.status_code

    def test_post_create_working_correctly(self):
        data = {
            'name': 'Test',
            'teachers': self.teacher.pk,
            'students': self.student.pk,
        }
        res = self.client.post(self.url, data)
        assert status.HTTP_201_CREATED == res.status_code
        assert 'Test' == Course.objects.last().name

    def test_teacher_can_not_be_student(self):
        data = {
            'name': 'Test',
            'teachers': self.teacher.pk,
            'students': self.teacher.pk,
        }
        res = self.client.post(self.url, data)
        assert status.HTTP_400_BAD_REQUEST == res.status_code
        assert "A person can't be teacher and student same time" == res.data['students'][0]
