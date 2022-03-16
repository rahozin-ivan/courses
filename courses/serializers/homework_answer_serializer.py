from rest_framework import serializers

from courses.models import HomeworkAnswer, Homework


class HomeworkAnswerSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = HomeworkAnswer
        fields = ('answer', 'user')

    def create(self, validated_data):
        homework_pk = self.context['view'].kwargs['homework_pk']
        validated_data['homework'] = Homework.objects.get(pk=homework_pk)
        obj = HomeworkAnswer.objects.create(**validated_data)
        return obj
