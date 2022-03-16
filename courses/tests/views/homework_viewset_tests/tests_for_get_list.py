from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from mixer.backend.django import mixer

from courses.models import Course, Lecture, Homework


class HomeworkViewSetTestsForGetListRequest(APITestCase):
    def setUp(self) -> None:
        self.teacher = mixer.blend(get_user_model(), role='Teacher')
        self.client.force_authenticate(self.teacher)
        self.course = mixer.blend(Course, teachers=self.teacher.pk)
        self.lecture = mixer.blend(Lecture, course=self.course)
        self.url = reverse('homework-list', kwargs={'course_pk': self.course.pk, 'lecture_pk': self.lecture.pk})

    def test_get_list_not_working_without_login(self):
        self.client.logout()
        res = self.client.get(self.url)
        assert status.HTTP_401_UNAUTHORIZED == res.status_code

    def test_get_list_not_working_for_not_course_users(self):
        self.client.force_authenticate(mixer.blend(get_user_model()))
        res = self.client.get(self.url)
        assert status.HTTP_403_FORBIDDEN == res.status_code

    def test_get_list_returning_all_homeworks_relate_to_lecture(self):
        mixer.cycle(5).blend(Homework, lecture=self.lecture)
        lecture = mixer.blend(Lecture)
        mixer.cycle(5).blend(Homework, lecture=lecture)
        res = self.client.get(self.url)
        assert status.HTTP_200_OK == res.status_code
        assert 5 == len(res.data)


