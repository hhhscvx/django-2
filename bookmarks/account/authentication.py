from django.contrib.auth.models import User


class EmailAuthBackend:
    """Аутентификация по адресу электронной почты"""

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(
                email=username)  # Если в имени указали адрес эл почты, то пытается найти его в БД по email`у
            if user.check_password(password):  # Проверяет правильный ли указан пароль, то успешная auth else None
                return user
            return None
        except (User.DoesNotExist,  # пользователь с указанной почтой не найден
                User.MultipleObjectsReturned):  # Найдено несколько пользователей с указанной почтой
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
