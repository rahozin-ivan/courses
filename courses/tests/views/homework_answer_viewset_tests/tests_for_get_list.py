from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from mixer.backend.django import mixer

from courses.models import Course, Lecture, Homework, HomeworkAnswer


class HomeworkAnswerViewSetTestsForGetListRequest(APITestCase):
    def setUp(self) -> None:
        self.teacher = mixer.blend(get_user_model(), role='Teacher')
        self.student = mixer.blend(get_user_model(), role='Student')
        self.client.force_authenticate(self.teacher)
        self.course = mixer.blend(Course, teachers=self.teacher.pk, students=self.student.pk)
        self.lecture = mixer.blend(Lecture, course=self.course)
        self.homework = mixer.blend(Homework, lecture=self.lecture)
        self.url = reverse('homework_answer-list', kwargs={'course_pk': self.course.pk,
                                                           'lecture_pk': self.lecture.pk,
                                                           'homework_pk': self.homework.pk})

    def test_get_list_not_working_without_login(self):
        self.client.logout()
        res = self.client.get(self.url)
        assert status.HTTP_401_UNAUTHORIZED == res.status_code

    def test_get_list_not_working_for_not_course_users(self):
        self.client.force_authenticate(mixer.blend(get_user_model()))
        res = self.client.get(self.url)
        assert status.HTTP_403_FORBIDDEN == res.status_code

    def test_get_list_returning_all_homeworks_answers_relate_to_homework(self):
        mixer.cycle(5).blend(HomeworkAnswer, homework=self.homework)
        homework = mixer.blend(Homework)
        mixer.cycle(5).blend(HomeworkAnswer, homework=homework)
        res = self.client.get(self.url)
        assert status.HTTP_200_OK == res.status_code
        assert 5 == len(res.data)

    def test_get_list_returning_all_homeworks_answers_relate_to_student(self):
        self.client.force_authenticate(self.student)
        mixer.cycle(5).blend(HomeworkAnswer, homework=self.homework, user=self.student)
        user = mixer.blend(get_user_model(), role='Student')
        self.course.students.add(user)
        mixer.cycle(5).blend(HomeworkAnswer, homework=self.homework, user=user)
        res = self.client.get(self.url)
        assert status.HTTP_200_OK == res.status_code
        assert 5 == len(res.data)
