from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course, Lesson, Subscription
from courses.paginators import LessonPaginator
from courses.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from courses.tasks import send_mail_update_course
from permissions import IsOwner, IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    """
        ViewSet-класс для вывода списка курсов и информации по одному объекту
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        """ Предоставляем права доступа в зависимости от роли"""
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
        """
            Определяем порядок создания нового курса, присваиваем владельца
        """
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()


class LessonCreateAPIView(generics.CreateAPIView):
    """
        Класс для создания урока. Доступно авторизованному пользователю, кроме модератора
    """
    serializer_class = LessonSerializer
    permission_classes = [~ IsModerator]

    def perform_create(self, serializer):
        """
            Определяем порядок создания нового урока, присваиваем владельца
        """
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        # Добавляем задачу по отправке письма об обновлении курса в обработчик celery
        send_mail_update_course.delay(new_lesson.course_id)
        new_lesson.save()

class LessonListAPIView(generics.ListAPIView):
    """
        Класс для вывода списка уроков. Доступно авторизованному пользователю
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
        Класс для вывода одного урока. Доступно владельцу, модератору, администратору
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator | IsAdminUser]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
        Класс для изменения урока. Доступно владельцу, модератору, администратору
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator | IsAdminUser]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
        Класс для удаления урока. Доступно владельцу, администратору
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsAdminUser]


class SubscribeCreateAPIView(generics.CreateAPIView):
    """
        Класс для создания подписки. Доступно авторизованным пользователям
    """
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Course.objects.all()

    def create(self, request, *args, **kwargs):
        """
            Определяем порядок создания нового объекта
        """
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
    """
        Класс для отмены подписки. Доступно авторизованным пользователям
    """
    serializer_class = SubscriptionSerializer

    def post(self, request,  *args, **kwargs):
        """
            Меняем статус подписки на неактивную
        """
        user = request.user
        course_id = self.kwargs['pk']
        # Устанавливаем подписку как неактивную
        subscription = Subscription.objects.filter(course=course_id, user=user).first()
        subscription.is_active = False
        subscription.save()
        return Response({"detail": "Вы отписаны."}, status=status.HTTP_200_OK)
