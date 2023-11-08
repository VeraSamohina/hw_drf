from django.urls import reverse
from rest_framework import status

from rest_framework.test import APITestCase, APIClient

from courses.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        # Тестовый пользователь
        self.client = APIClient()
        self.user = User.objects.create(email='user@test.com', password='12345')
        self.client.force_authenticate(user=self.user)

        # Тестовый курс
        self.course = Course.objects.create(title='test_course')

        # Тестовый урок
        self.lesson = Lesson.objects.create(title='lesson1', course=self.course, owner=self.user)

    def test_create_lesson(self):
        """Тестирование создания урока"""
        data = {
            'title': 'test',
            'description': 'test',
            'course': 1
        }
        response = self.client.post(reverse('courses:lesson-create'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], data['title'])
        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_list_lesson(self):
        """Тестирование вывода списка уроков"""
        response = self.client.get(reverse('courses:lesson-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_lesson(self):
        """Тестирование вывода одного урока"""
        response = self.client.get(reverse('courses:lesson-detail', args=[self.lesson.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], 'lesson1')

    def test_update_lesson(self):
        """Тестирование изменения урока"""
        data = {
            'title': 'update_lesson1'}

        response = self.client.patch(reverse('courses:lesson-update', args=[self.lesson.id]), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], 'update_lesson1')

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        response = self.client.delete(reverse('courses:lesson-delete', args=[self.lesson.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        # Тестовый пользователь
        self.client = APIClient()
        self.user = User.objects.create(email='user@test.com', password='12345')
        self.client.force_authenticate(user=self.user)

        # Тестовый курс
        self.course = Course.objects.create(title='test_course')

    def test_subscribe(self):
        """Тестирование подписки на курс"""
        data = {'course': self.course, 'user': self.user}
        response = self.client.post(reverse('courses:subscribe-course', args=[self.course.id]), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unsubscribe(self):
        """Тестирование отмены подписки на курс"""
        self.course_subscription = Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post(reverse('courses:unsubscribe-course', args=[self.course.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(is_active=True).exists())
