from rest_framework import serializers

from courses.models import Comment, Mark


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('comment', 'user')

    def create(self, validated_data):
        mark = Mark.objects.get(pk=self.context['view'].kwargs['mark_pk'])
        validated_data['mark'] = mark
        obj = Comment.objects.create(**validated_data)
        return obj
