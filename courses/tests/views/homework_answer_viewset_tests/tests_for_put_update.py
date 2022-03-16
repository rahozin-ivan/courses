from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from mixer.backend.django import mixer

from courses.models import Course, Lecture, Homework, HomeworkAnswer


class HomeworkAnswerViewSetTestsForPutUpdateRequest(APITestCase):
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

    def test_put_update_not_working_without_login(self):
        self.client.logout()
        res = self.client.put(self.url)
        assert status.HTTP_401_UNAUTHORIZED == res.status_code

    def test_put_update_not_working_for_not_course_users(self):
        self.client.force_authenticate(mixer.blend(get_user_model()))
        res = self.client.put(self.url)
        assert status.HTTP_404_NOT_FOUND == res.status_code

    def test_delete_destroy_not_working_for_course_teachers(self):
        self.client.force_authenticate(self.teacher)
        res = self.client.delete(self.url)
        assert status.HTTP_403_FORBIDDEN == res.status_code

    def test_put_update_working_correctly(self):
        data = {
            'answer': 'Test',
        }
        res = self.client.put(self.url, data)
        self.homework_answer.refresh_from_db()
        assert status.HTTP_200_OK == res.status_code
        assert 'Test' == self.homework_answer.answer
