from rest_framework import serializers

from courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'teachers', 'students')

    def validate(self, attrs):
        teachers = attrs.get('teachers')
        students = attrs.get('students')
        if teachers and students:
            if set(teachers).intersection(students):
                raise serializers.ValidationError({'students': "A person can't be teacher and student same time"})
        return attrs
