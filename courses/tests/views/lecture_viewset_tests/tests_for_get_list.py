from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from mixer.backend.django import mixer

from courses.models import Course, Lecture


class LectureViewSetTestsForGetListRequest(APITestCase):
    def setUp(self) -> None:
        self.teacher = mixer.blend(get_user_model(), role='Teacher')
        self.client.force_authenticate(self.teacher)
        self.course = mixer.blend(Course, teachers=self.teacher.pk)
        self.url = reverse('lecture-list', args=[self.course.pk])

    def test_get_list_not_working_without_login(self):
        self.client.logout()
        res = self.client.get(self.url)
        assert status.HTTP_401_UNAUTHORIZED == res.status_code

    def test_get_list_not_working_for_not_course_users(self):
        self.client.force_authenticate(mixer.blend(get_user_model()))
        res = self.client.get(self.url)
        assert status.HTTP_403_FORBIDDEN == res.status_code

    def test_get_list_returning_all_lectures_relate_to_course(self):
        mixer.cycle(5).blend(Lecture, course=self.course)
        course = mixer.blend(Course)
        mixer.cycle(5).blend(Lecture, course=course)
        res = self.client.get(self.url)
        assert status.HTTP_200_OK == res.status_code
        assert 5 == len(res.data)


