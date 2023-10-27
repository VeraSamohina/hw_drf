from django.contrib import admin

from payments.models import Payment
from users.models import User

admin.site.register(Payment)
admin.site.register(User)
