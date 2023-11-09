from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from courses.models import Course, Lesson, Subscription
from courses.validators import LinkOnlyYoutubeValidator


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = SerializerMethodField()
    lesson_list = SerializerMethodField()
    subscribe_status = SerializerMethodField()

    def get_count_lessons(self, course):
        return course.lesson_set.count()

    def get_lesson_list(self, course):
        return [lesson.title for lesson in Lesson.objects.filter(course=course)]

    def get_subscribe_status(self, course):
        request = self.context.get('request')
        if Subscription.objects.filter(course=course, is_active=True, user=request.user).exists():
            return "Вы подписаны на обновления этого курса"
        return "Подписка не оформлена"

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    validators = [LinkOnlyYoutubeValidator(field='video')]

    class Meta:
        model = Lesson
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
