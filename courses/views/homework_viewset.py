from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from courses.serializers import HomeworkSerializer
from courses.models import Lecture
from courses.permissions import IsCourseTeacher


class HomeworkViewSet(ModelViewSet):
    serializer_class = HomeworkSerializer
    permission_classes = (IsAuthenticated, IsCourseTeacher)

    def get_queryset(self):
        return Lecture.objects.get(pk=self.kwargs['lecture_pk']).homeworks.all()
