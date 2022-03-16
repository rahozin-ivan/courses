from django.core.files import File
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from mock import mock

from mixer.backend.django import mixer

from courses.models import Course, Lecture


class LectureViewSetTestsForPutUpdateRequest(APITestCase):
    def setUp(self) -> None:
        self.teacher = mixer.blend(get_user_model(), role='Teacher')
        self.student = mixer.blend(get_user_model(), role='Student')
        self.client.force_authenticate(self.teacher)
        self.course = mixer.blend(Course, teachers=self.teacher.pk, students=self.student.pk)
        self.lecture = mixer.blend(Lecture, course=self.course)
        self.url = reverse('lecture-detail', kwargs={'course_pk': self.course.pk, 'pk': self.lecture.pk})

    def test_put_update_not_working_without_login(self):
        self.client.logout()
        res = self.client.put(self.url)
        assert status.HTTP_401_UNAUTHORIZED == res.status_code

    def test_put_update_not_working_for_not_course_users(self):
        self.client.force_authenticate(mixer.blend(get_user_model()))
        res = self.client.put(self.url)
        assert status.HTTP_403_FORBIDDEN == res.status_code

    def test_put_update_not_working_for_course_students(self):
        self.client.force_authenticate(self.student)
        res = self.client.put(self.url)
        assert status.HTTP_403_FORBIDDEN == res.status_code

    def test_put_update_working_correctly(self):
        data = {
            'name': 'Test',
            'presentation': mock.MagicMock(spec=File),
        }
        res = self.client.put(self.url, data)
        self.lecture.refresh_from_db()
        assert status.HTTP_200_OK == res.status_code
        assert 'Test' == self.lecture.name
