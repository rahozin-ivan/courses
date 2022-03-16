from rest_framework import serializers

from courses.models import Mark, HomeworkAnswer


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ('mark', )

    def create(self, validated_data):
        homework_answer = HomeworkAnswer.objects.get(pk=self.context['view'].kwargs['homework_answer_pk'])
        validated_data['homework_answer'] = homework_answer
        if Mark.objects.filter(homework_answer=homework_answer).exists():
            raise serializers.ValidationError("You can't create 2 marks on 1 answer")
        obj = Mark.objects.create(**validated_data)
        return obj
