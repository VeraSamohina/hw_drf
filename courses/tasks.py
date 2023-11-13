import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from courses.models import Course, Subscription
from users.models import User


@shared_task
def send_mail_update_course(course_id):
    """
        Отправка сообщения подписчику курса о выходе новых уроков
    """
    course = Course.objects.get(pk=course_id)
    subscriptions = Subscription.objects.filter(course=course_id, is_active=True)
    for subscription in subscriptions:
        send_mail(subject=f'Вышли обновления курса {course}',
                  message=f'Вы получили это письмо, потому что подписаны на обновления курса {course}. Посмотрите новые материалы',
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[subscription.user.email],
                  fail_silently=False)


@shared_task
def inactivate_user():
    """
        Периодическая задача - проверка активности пользователя (блокировка если нет активности 30 дней)
    """
    date_x = datetime.datetime.today() - datetime.timedelta(days=30)
    filter_active = {'last_login__lte': date_x}
    inactive_users = User.objects.filter(**filter_active, is_active=True)
    for user in inactive_users:
        print(f' пользователь{user} будет заблокирован')
        user.is_active = False
        user.save()
