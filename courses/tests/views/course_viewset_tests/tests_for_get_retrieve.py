from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from mixer.backend.django import mixer

from courses.models import Course


class CourseViewSetTestsForGetRetrieve(APITestCase):
    def setUp(self) -> None:
        self.teacher = mixer.blend(get_user_model(), role='Teacher')
        self.client.force_authenticate(self.teacher)
        self.course = mixer.blend(Course, teachers=self.teacher.pk)
        self.url = reverse('course-detail', args=[self.course.pk])

    def test_get_retrieve_not_working_without_login(self):
        self.client.logout()
        res = self.client.get(self.url)
        assert status.HTTP_401_UNAUTHORIZED == res.status_code

    def test_get_retrieve_not_working_for_not_course_users(self):
        self.client.force_authenticate(mixer.blend(get_user_model()))
        res = self.client.get(self.url)
        assert status.HTTP_404_NOT_FOUND == res.status_code

    def test_get_retrieve_working_correctly(self):
        res = self.client.get(self.url)
        assert status.HTTP_200_OK == res.status_code
        assert self.course.name == res.data['name']
