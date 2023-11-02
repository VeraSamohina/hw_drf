import re

from rest_framework.serializers import ValidationError


class LinkOnlyYoutubeValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        video_url = value.get(self.field)
        if not video_url.startswith('https://www.youtube.com/'):
            raise ValidationError('Запрещено использовать ссылки на ресурсы, кроме Youtube')
