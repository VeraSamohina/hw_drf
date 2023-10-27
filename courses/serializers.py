from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from courses.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = SerializerMethodField()

    def get_count_lessons(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
