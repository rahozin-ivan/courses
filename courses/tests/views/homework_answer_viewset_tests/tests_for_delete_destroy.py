from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from mixer.backend.django import mixer

from courses.models import Course, Lecture, Homework, HomeworkAnswer


class HomeworkAnswerViewSetTestsForDeleteDestroyRequest(APITestCase):
    def setUp(self) -> None:
        self.teacher = mixer.blend(get_user_model(), role='Teacher')
        self.student = mixer.blend(get_user_model(), role='Student')
        self.client.force_authenticate(self.student)
        self.course = mixer.blend(Course, teachers=self.teacher.pk, students=self.student.pk)
        self.lecture = mixer.blend(Lecture, course=self.course)
        self.homework = mixer.blend(Homework, lecture=self.lecture)
        self.homework_answer = mixer.blend(HomeworkAnswer, homework=self.homework, user=self.student)
        self.url = reverse('homework_answer-detail', kwargs={'course_pk': self.course.pk,
                                                             'lecture_pk': self.lecture.pk,
                                                             'homework_pk': self.homework.pk,
                                                             'pk': self.homework_answer.pk})

    def test_delete_destroy_not_working_without_login(self):
        self.client.logout()
        res = self.client.delete(self.url)
        assert status.HTTP_401_UNAUTHORIZED == res.status_code

    def test_delete_destroy_not_working_for_not_course_users(self):
        self.client.force_authenticate(mixer.blend(get_user_model()))
        res = self.client.delete(self.url)
        assert status.HTTP_404_NOT_FOUND == res.status_code

    def test_delete_destroy_not_working_for_course_teachers(self):
        self.client.force_authenticate(self.teacher)
        res = self.client.delete(self.url)
        assert status.HTTP_403_FORBIDDEN == res.status_code

    def test_delete_destroy_working_correctly(self):
        homework_answer_pk = self.homework_answer.pk
        res = self.client.delete(self.url)
        assert status.HTTP_204_NO_CONTENT == res.status_code
        assert False == HomeworkAnswer.objects.filter(pk=homework_answer_pk).exists()
