from django.contrib import admin
from .models import Profile

# Включаем в сайт администрации управление профилями
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
    raw_id_fields = ['user']