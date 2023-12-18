from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,  #
                                on_delete=models.CASCADE)  # Удаляем Profile при удалении user
    date_of_birth = models.DateField(blank=True, null=True)  # Может быть пустым и иметь значение null
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              # путь, в котором будут сохранены загруженные изображения (аватарки); (users/2023/12/18)
                              blank=True)

    def __str__(self):
        return f'Профиль пользователя - {self.user.username}'
