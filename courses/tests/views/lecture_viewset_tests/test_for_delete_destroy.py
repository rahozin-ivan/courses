from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from mixer.backend.django import mixer

from courses.models import Course, Lecture


class LectureViewSetTestsForDeleteDestroyRequest(APITestCase):
    def setUp(self) -> None:
        self.teacher = mixer.blend(get_user_model(), role='Teacher')
        self.student = mixer.blend(get_user_model(), role='Student')
        self.client.force_authenticate(self.teacher)
        self.course = mixer.blend(Course, teachers=self.teacher.pk, students=self.student.pk)
        self.lecture = mixer.blend(Lecture, course=self.course)
        self.url = reverse('lecture-detail', kwargs={'course_pk': self.course.pk, 'pk': self.lecture.pk})

    def test_delete_destroy_not_working_without_login(self):
        self.client.logout()
        res = self.client.delete(self.url)
        assert status.HTTP_401_UNAUTHORIZED == res.status_code

    def test_delete_destroy_not_working_for_not_course_users(self):
        self.client.force_authenticate(mixer.blend(get_user_model()))
        res = self.client.delete(self.url)
        assert status.HTTP_403_FORBIDDEN == res.status_code

    def test_delete_destroy_not_working_for_course_students(self):
        self.client.force_authenticate(self.student)
        res = self.client.delete(self.url)
        assert status.HTTP_403_FORBIDDEN == res.status_code

    def test_delete_destroy_working_correctly(self):
        lecture_pk = self.lecture.pk
        res = self.client.delete(self.url)
        assert status.HTTP_204_NO_CONTENT == res.status_code
        assert False == Lecture.objects.filter(pk=lecture_pk).exists()
