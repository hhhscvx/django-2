from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image


@receiver(m2m_changed, sender=Image.users_like.through)  # связывает сигнал изменения с users_like
def users_like_changed(sender, instance, **kwargs):
    # вызывается при сигнале, sender - отправитель сигнала, instance - экземпляр модели, который инициировал сигнал
    instance.total_likes = instance.users_like.count()
    instance.save()
