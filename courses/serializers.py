from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from courses.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = SerializerMethodField()
    lesson_list = SerializerMethodField()

    def get_count_lessons(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_lesson_list(self, course):
        return [lesson.title for lesson in Lesson.objects.filter(course=course)]

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
