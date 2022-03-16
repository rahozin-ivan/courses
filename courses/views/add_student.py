from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from courses.models import Course
from users.serializers import UserSerializer
from courses.permissions import IsCourseTeacher


class CourseAddStudentView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsCourseTeacher)

    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs.get('course_pk'))
        email = request.data.get('email')

        if get_user_model().objects.filter(email=email).exists():
            user = get_user_model().objects.get(email=email)
        else:
            return Response(f'Пользователя с таким {email=} не существует', status=status.HTTP_404_NOT_FOUND)

        if user not in course.teachers.all():
            course.students.add(user.pk)
            return Response(f'{user} успешно добавлен на курс', status=201)
        return Response(f'Пользователь с таким {email=} является преподавателем', status=status.HTTP_404_NOT_FOUND)
