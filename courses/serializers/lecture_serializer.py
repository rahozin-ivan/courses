from rest_framework import serializers

from courses.models import Lecture, Course


class LectureSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Lecture
        fields = ('name', 'presentation', 'user')

    def create(self, validated_data):
        course_pk = self.context['view'].kwargs['course_pk']
        validated_data['course'] = Course.objects.get(pk=course_pk)
        obj = Lecture.objects.create(**validated_data)
        return obj
