import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action


def create_action(user, verb, target=None):
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id,
                                            verb=verb,
                                            created__gte=last_minute)
    if target:  # если было выполнено (указано) действие
        target_ct = ContentType.objects.get_for_model(target)  # само действие, берется модель target`а
        similar_actions = similar_actions.filter(target_ct=target_ct,  # доп. фильтрация одинаковых целей одним user`ом
                                                 target_id=target.id)

    if not similar_actions:  # similar_actions - одинаковые действия, выполненные одним и тем же user`ом за ласт минуту
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True  # boolean о том, было ли действие сохранено
    return False
