from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from mixer.backend.django import mixer

from courses.models import Course


class AddTeacherViewTests(APITestCase):
    def setUp(self) -> None:
        self.teacher = mixer.blend(get_user_model(), role='Teacher')
        self.student = mixer.blend(get_user_model(), role='Student')
        self.client.force_authenticate(self.teacher)
        self.course = mixer.blend(Course, teachers=self.teacher.pk, students=self.student.pk)
        self.url = reverse('course_add_teacher', args=[self.course.pk])

    def test_add_teacher_view_not_working_without_login(self):
        self.client.logout()
        res = self.client.post(self.url)
        assert status.HTTP_401_UNAUTHORIZED == res.status_code

    def test_add_teacher_view_not_working_for_not_course_users(self):
        self.client.force_authenticate(mixer.blend(get_user_model()))
        res = self.client.post(self.url)
        assert status.HTTP_403_FORBIDDEN == res.status_code

    def test_add_teacher_view_not_working_for_course_students(self):
        self.client.force_authenticate(self.student)
        res = self.client.post(self.url)
        assert status.HTTP_403_FORBIDDEN == res.status_code

    def test_add_teacher_view_working_correctly(self):
        user = mixer.blend(get_user_model(), role='Teacher')
        data = {
            'email': user.email,
        }
        res = self.client.post(self.url, data)
        assert status.HTTP_201_CREATED == res.status_code
        assert f'{user} успешно добавлен на курс' == res.data

    def test_add_teacher_view_not_working_when_teacher_does_not_exists(self):
        email = 'notemail'
        data = {
            'email': email,
        }
        res = self.client.post(self.url, data)
        assert status.HTTP_404_NOT_FOUND == res.status_code
        assert f'Пользователя с таким {email=} не существует' == res.data

    def test_add_teacher_view_not_working_if_user_already_course_student(self):
        user = mixer.blend(get_user_model(), role='Teacher')
        email = user.email
        self.course.students.add(user)
        data = {
            'email': email,
        }
        res = self.client.post(self.url, data)
        assert status.HTTP_404_NOT_FOUND == res.status_code
        assert f'Пользователь с таким {email=} является студентом этого курса или не является преподавателем' == \
               res.data

    def test_add_teacher_view_not_working_if_user_not_teacher(self):
        user = mixer.blend(get_user_model(), role='Student')
        email = user.email
        data = {
            'email': email,
        }
        res = self.client.post(self.url, data)
        assert status.HTTP_404_NOT_FOUND == res.status_code
        assert f'Пользователь с таким {email=} является студентом этого курса или не является преподавателем' == \
               res.data
