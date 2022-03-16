from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from mixer.backend.django import mixer

from courses.models import Course


class CourseViewSetTestsForGetListRequest(APITestCase):
    def setUp(self) -> None:
        self.teacher = mixer.blend(get_user_model(), role='Teacher')
        self.client.force_authenticate(self.teacher)
        self.url = reverse('course-list')

    def test_get_list_returning_all_courses_relate_to_user(self):
        mixer.cycle(5).blend(Course, teachers=self.teacher.pk)
        user = mixer.blend(get_user_model())
        mixer.cycle(5).blend(Course, teachers=user.pk)
        res = self.client.get(self.url)
        assert status.HTTP_200_OK == res.status_code
        assert 5 == len(res.data)

    def test_get_list_not_working_without_login(self):
        self.client.logout()
        res = self.client.get(self.url)
        assert status.HTTP_401_UNAUTHORIZED == res.status_code
