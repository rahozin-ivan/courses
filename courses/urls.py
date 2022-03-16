from django.urls import path, include

from rest_framework_nested import routers

from courses import views

course_router = routers.SimpleRouter()
course_router.register('', views.CourseViewSet, basename='course')

lecture_router = routers.NestedSimpleRouter(course_router, '', lookup='course')
lecture_router.register('lectures', views.LectureViewSet, basename='lecture')

homework_router = routers.NestedSimpleRouter(lecture_router, 'lectures', lookup='lecture')
homework_router.register('homeworks', views.HomeworkViewSet, basename='homework')

homework_answer_router = routers.NestedSimpleRouter(homework_router, 'homeworks', lookup='homework')
homework_answer_router.register('answers', views.HomeworkAnswerViewSet, basename='homework_answer')

mark_router = routers.NestedSimpleRouter(homework_answer_router, 'answers', lookup='homework_answer')
mark_router.register('marks', views.MarkViewSet, basename='mark')

comment_router = routers.NestedSimpleRouter(mark_router, 'marks', lookup='mark')
comment_router.register('comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(course_router.urls)),
    path('', include(lecture_router.urls)),
    path('', include(homework_router.urls)),
    path('', include(homework_answer_router.urls)),
    path('', include(mark_router.urls)),
    path('', include(comment_router.urls)),
    path('<int:course_pk>/add-student/', views.CourseAddStudentView.as_view(), name='course_add_student'),
    path('<int:course_pk>/add-teacher/', views.CourseAddTeacherView.as_view(), name='course_add_teacher'),
]
