from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from courses import permissions
from courses.models import Homework, Course, Mark
from courses.serializers import MarkSerializer


class MarkViewSet(ModelViewSet):
    serializer_class = MarkSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = (IsAuthenticated, permissions.IsCourseTeacher)
        else:
            self.permission_classes = (IsAuthenticated, permissions.IsCourseTeacherOrHomeworkAnswerOwner)
        return super().get_permissions()

    def get_queryset(self):
        homework = Homework.objects.get(pk=self.kwargs['homework_pk'])
        course = Course.objects.get(pk=self.kwargs['course_pk'])
        if self.request.user in course.teachers.all():
            return Mark.objects.filter(homework_answer__homework=homework)
        else:
            return Mark.objects.filter(homework_answer__user=self.request.user)
