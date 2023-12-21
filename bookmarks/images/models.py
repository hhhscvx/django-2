from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  # Указывает на auth на данный момент пользователя
                             related_name='images_created',  # по этому имени обращаемся к связанным images с user`ом
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=24)
    slug = models.SlugField(max_length=24,
                            blank=True)
    image = models.ImageField(upload_to='%Y/%m/%d')
    url = models.URLField()
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)  # auto_now_add - устанавлеваем now время и дату при создании
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,  # Многие ко многим понравившееся image и user`ы
                                        related_name='images_liked',
                                        blank=True)

    class Meta:
        indexes = [
            # короче походу это надо так как чаще обращаемся к более свежим image`ам, будет сортировано сразу по created
            models.Index(fields=['-created'])
        ]
        ordering = ['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # делаем slug по title`у
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])  # ссылаемся на urls detail через section images
