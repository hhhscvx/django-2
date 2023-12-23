from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,  #
                                on_delete=models.CASCADE)  # Удаляем Profile при удалении user
    date_of_birth = models.DateField(blank=True, null=True)  # Может быть пустым и иметь значение null
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              # путь, в котором будут сохранены загруженные изображения (аватарки); (users/2023/12/18)
                              blank=True)

    def __str__(self):
        return f'Профиль пользователя - {self.user.username}'


class Contact(models.Model):
    user_from = models.ForeignKey('auth.User',  # пользователь, который создает взаимосвязь
                                  related_name="rel_from_set",
                                  on_delete=models.CASCADE)

    user_to = models.ForeignKey('auth.User',  # пользователь, на которого он подписывается
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created'])
        ]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} follow {self.user_to}'


user_model = get_user_model()
user_model.add_to_class('following',  # добавляем к модели пользователя following = ManyToManyField кот.связан с Contact
                        models.ManyToManyField('self',
                                               through=Contact,
                                               related_name='followers',
                                               symmetrical=False))  # для того чтобы если 1 подписывается на 2, не означало что 2 тоже подписывается на 1
