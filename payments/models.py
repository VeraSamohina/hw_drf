from django.db import models

from config import settings
from courses.models import Course, Lesson


class Payment(models.Model):
    class PaymentType(models.TextChoices):
        CACHE = "CACHE", "Наличные"
        TRANSFER_TO_ACCOUNT = "TRANSFER_TO_ACCOUNT", "Перевод на счет"
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='payment')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, related_name='payment')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    date = models.DateTimeField(verbose_name='дата платежа')
    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='сумма платежа')
    payment_type = models.CharField(choices=PaymentType.choices)

    def __str__(self):
        return f'{self.date} - {self.amount}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
