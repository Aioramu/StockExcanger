from django.contrib import admin

# Register your models here.
from .models import Stock,Financial
admin.site.register(Stock)
admin.site.register(Financial)
