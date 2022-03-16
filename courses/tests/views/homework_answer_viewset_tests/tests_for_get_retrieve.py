from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from mixer.backend.django import mixer

from courses.models import Course, Lecture, Homework, HomeworkAnswer


class HomeworkAnswerViewSetTestsForGetRetrieve(APITestCase):
    def setUp(self) -> None:
        self.teacher = mixer.blend(get_user_model(), role='Teacher')
        self.student = mixer.blend(get_user_model(), role='Student')
        self.client.force_authenticate(self.teacher)
        self.course = mixer.blend(Course, teachers=self.teacher.pk, students=self.student.pk)
        self.lecture = mixer.blend(Lecture, course=self.course)
        self.homework = mixer.blend(Homework, lecture=self.lecture)
        self.homework_answer = mixer.blend(HomeworkAnswer, homework=self.homework, user=self.student)
        self.url = reverse('homework_answer-detail', kwargs={'course_pk': self.course.pk,
                                                             'lecture_pk': self.lecture.pk,
                                                             'homework_pk': self.homework.pk,
                                                             'pk': self.homework_answer.pk})

    def test_get_retrieve_not_working_without_login(self):
        self.client.logout()
        res = self.client.get(self.url)
        assert status.HTTP_401_UNAUTHORIZED == res.status_code

    def test_get_retrieve_not_working_for_not_course_users(self):
        self.client.force_authenticate(mixer.blend(get_user_model()))
        res = self.client.get(self.url)
        assert status.HTTP_404_NOT_FOUND == res.status_code

    def test_get_retrieve_not_working_for_other_students(self):
        user = mixer.blend(get_user_model())
        self.course.students.add(user)
        self.client.force_authenticate(user)
        res = self.client.get(self.url)
        assert status.HTTP_404_NOT_FOUND == res.status_code

    def test_get_retrieve_working_correctly(self):
        res = self.client.get(self.url)
        assert status.HTTP_200_OK == res.status_code
        assert self.homework_answer.answer == res.data['answer']
