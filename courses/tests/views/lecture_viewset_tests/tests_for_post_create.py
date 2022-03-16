from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files import File

from rest_framework import status
from rest_framework.test import APITestCase

from mixer.backend.django import mixer

from mock import mock

from courses.models import Course, Lecture


class LectureViewSetTestsForPostCreateRequest(APITestCase):
    def setUp(self) -> None:
        self.teacher = mixer.blend(get_user_model(), role='Teacher')
        self.student = mixer.blend(get_user_model(), role='Student')
        self.client.force_authenticate(self.teacher)
        self.course = mixer.blend(Course, teachers=self.teacher.pk, students=self.student.pk)
        self.url = reverse('lecture-list', kwargs={'course_pk': self.course.pk})

    def test_post_create_not_working_without_login(self):
        self.client.logout()
        res = self.client.post(self.url)
        assert status.HTTP_401_UNAUTHORIZED == res.status_code

    def test_post_create_not_working_for_not_course_users(self):
        self.client.force_authenticate(mixer.blend(get_user_model()))
        res = self.client.post(self.url)
        assert status.HTTP_403_FORBIDDEN == res.status_code

    def test_post_create_not_working_for_students(self):
        self.client.force_authenticate(self.student)
        res = self.client.post(self.url)
        assert status.HTTP_403_FORBIDDEN == res.status_code

    def test_post_create_working_correctly(self):
        data = {
            'name': 'Test',
            'presentation': mock.MagicMock(spec=File),
        }
        res = self.client.post(self.url, data)
        assert status.HTTP_201_CREATED == res.status_code
        assert 'Test' == Lecture.objects.last().name
