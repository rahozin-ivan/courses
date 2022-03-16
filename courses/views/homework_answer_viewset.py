from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from courses import permissions
from courses.serializers import HomeworkAnswerSerializer
from courses.models import Homework, HomeworkAnswer, Course


class HomeworkAnswerViewSet(ModelViewSet):
    serializer_class = HomeworkAnswerSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = (IsAuthenticated, permissions.IsCourseStudent)
        elif self.action in ['retrieve']:
            self.permission_classes = (IsAuthenticated, permissions.IsHomeworkAnswerOwnerOrCourseTeacher)
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = (IsAuthenticated, permissions.IsHomeworkAnswerOwner)
        else:
            self.permission_classes = (IsAuthenticated, permissions.IsCourseTeacher)
        return super().get_permissions()

    def get_queryset(self):
        homework = Homework.objects.get(pk=self.kwargs['homework_pk'])
        course = Course.objects.get(pk=self.kwargs['course_pk'])
        if self.request.user in course.teachers.all():
            return HomeworkAnswer.objects.filter(homework=homework)
        else:
            return HomeworkAnswer.objects.filter(user=self.request.user)
