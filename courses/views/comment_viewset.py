from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from courses.serializers import CommentSerializer
from courses.permissions import IsCourseTeacherOrHomeworkAnswerOwner, IsCommentOwner
from courses.models import Mark


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = (IsAuthenticated, IsCourseTeacherOrHomeworkAnswerOwner)
        else:
            self.permission_classes = (IsAuthenticated, IsCommentOwner)
        return super().get_permissions()

    def get_queryset(self):
        return Mark.objects.get(pk=self.kwargs['mark_pk']).comments.all()
