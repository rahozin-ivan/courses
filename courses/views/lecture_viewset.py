from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from courses.models import Lecture
from courses.serializers import LectureSerializer
from courses.permissions import IsCourseTeacher


class LectureViewSet(ModelViewSet):
    serializer_class = LectureSerializer
    permission_classes = (IsAuthenticated, IsCourseTeacher)

    def get_queryset(self):
        return Lecture.objects.filter(course=self.kwargs['course_pk'])
