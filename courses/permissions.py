from rest_framework import permissions

from courses.models import Course, HomeworkAnswer
from users.models import User


class IsTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == User.RoleChoices.TEACHER


class IsCourseTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        course = Course.objects.get(pk=view.kwargs['course_pk'])
        if course not in Course.objects.user_courses(request.user):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user in course.teachers.all()


class IsCourseTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS and \
           view.get_object() in Course.objects.user_courses(request.user):
            return True
        return request.user in view.get_object().teachers.all()


class IsCourseStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        course = Course.objects.get(pk=view.kwargs['course_pk'])
        return request.user in course.students.all()


class IsHomeworkAnswerOwnerOrCourseTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        course = Course.objects.get(pk=view.kwargs['course_pk'])
        return request.user == view.get_object().user or request.user in course.teachers.all()


class IsHomeworkAnswerOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user == view.get_object().user


class IsCourseTeacherOrHomeworkAnswerOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        course = Course.objects.get(pk=view.kwargs['course_pk'])
        homework_answer = HomeworkAnswer.objects.get(pk=view.kwargs['homework_answer_pk'])
        return request.user == homework_answer.user or request.user in course.teachers.all()


class IsCommentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
