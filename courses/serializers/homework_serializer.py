from rest_framework.serializers import ModelSerializer

from courses.models import Homework, Lecture


class HomeworkSerializer(ModelSerializer):
    class Meta:
        model = Homework
        fields = ('task', )

    def create(self, validated_data):
        lecture = Lecture.objects.get(pk=self.context['view'].kwargs['lecture_pk'])
        validated_data['lecture'] = lecture
        obj = Homework.objects.create(**validated_data)
        return obj
