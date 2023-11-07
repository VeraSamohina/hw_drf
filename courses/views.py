from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course, Lesson, Subscription
from courses.paginators import LessonPaginator
from courses.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from permissions import IsOwner, IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [IsOwner | IsModerator | IsAdminUser]
        elif self.action == 'create':
            permission_classes = [~ IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsOwner | IsAdminUser]
        elif self.action == 'update':
            permission_classes = [IsOwner | IsModerator | IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def partial_update(self, request, *args, **kwargs):
        pass


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~ IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator | IsAdminUser]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator | IsAdminUser]


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsAdminUser]


class SubscribeCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.all()

    def create(self, request, *args, **kwargs):
        course = self.get_object()
        user = request.user
        # Проверяем подписку на курс
        if Subscription.objects.filter(user=user, course=course, is_active=True).exists():
            return Response({"detail": "Вы уже подписаны на этот курс."}, status=status.HTTP_400_BAD_REQUEST)
        # Создаем подписку
        subscription = Subscription(user=user, course=course)
        subscription.save()

        return Response({"detail": "Подписка успешно установлена."}, status=status.HTTP_201_CREATED)


class UnSubscribeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        user = request.user
        # Устанавливаем подписку как неактивную
        subscription = Subscription.objects.filter(course=course_id, user=user).first()
        subscription.is_active = False
        subscription.save()
        return Response({"detail": "Вы отписаны."}, status=status.HTTP_200_OK)
