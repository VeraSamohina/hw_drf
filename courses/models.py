from django.db import models

from users.models import NULLABLE


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='courses/', verbose_name='изображение', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='lessons/', verbose_name='изображение', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    video = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, verbose_name='курс', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return self.title
