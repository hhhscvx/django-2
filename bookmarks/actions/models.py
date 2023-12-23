from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
    user = models.ForeignKey('auth.User',  # аутентифицированный на данный момент пользователь (модель User из auth)
                             related_name='actions',
                             on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)  # глагол для хранения инфы о действиях пользователя (X что-то сделал)
    created = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(ContentType,  # X что-то сделал
                                  blank=True, null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE)  # удалится пользователь - удалятся и его действия
    target_id = models.PositiveIntegerField(null=True, blank=True)  # тот самый X
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['target_ct', 'target_id']),
        ]
        ordering = ['-created']
