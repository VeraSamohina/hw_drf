from django.urls import path
from rest_framework.routers import DefaultRouter

from courses.apps import CoursesConfig
from courses.views import CourseViewSet, LessonCreateAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView, LessonListAPIView

app_name = CoursesConfig.name

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='courses')

urlpatterns = [path('lessons/create/', LessonCreateAPIView.as_view()),
               path('lessons/', LessonListAPIView.as_view()),
               path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view()),
               path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view()),
               path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view())
               ] + router.urls
