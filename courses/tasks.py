from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from courses.models import Course, Subscription


@shared_task
def send_mail_update_course(course_id):
    course = Course.objects.get(pk=course_id)
    subscriptions = Subscription.objects.filter(course=course_id, is_active=True)
    for subscription in subscriptions:
        send_mail(subject=f'Вышли обновления курса {course}',
                  message=f'Вы получили это письмо, потому что подписаны на обновления курса {course}. Посмотрите новые материалы',
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[subscription.user.email],
                  fail_silently=False)
