from django.urls import path
from rest_framework.routers import DefaultRouter

from courses.apps import CoursesConfig
from courses.views import CourseViewSet, LessonCreateAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView, LessonListAPIView, SubscribeCreateAPIView, UnSubscribeAPIView

app_name = CoursesConfig.name

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='courses')

urlpatterns = [path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
               path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
               path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
               path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
               path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
               path('courses/<int:pk>/subscribe/', SubscribeCreateAPIView.as_view(), name='subscribe-course'),
               path('courses/<int:pk>/unsubscribe/', UnSubscribeAPIView.as_view(), name='unsubscribe-course')
               ] + router.urls
