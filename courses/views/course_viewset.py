from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from courses.models import Course
from courses.serializers import CourseSerializer
from courses.permissions import IsCourseTeacherOrReadOnly, IsTeacherOrReadOnly
from courses.filters import CourseFilter


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filter_class = CourseFilter

    def get_queryset(self):
        return Course.objects.user_courses(self.request.user)

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = (IsAuthenticated, IsTeacherOrReadOnly)
        elif self.action in ['list']:
            self.permission_classes = (IsAuthenticated, )
        else:
            self.permission_classes = (IsAuthenticated, IsCourseTeacherOrReadOnly)
        return super().get_permissions()
