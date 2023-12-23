from django import forms
from .models import Image
from django.core.files.base import ContentFile
from django.utils.text import slugify
import requests


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extensions = url.rsplit('.', 1)[1].lower()
        if extensions not in valid_extensions:
            raise forms.ValidationError('Формат файла некорректен')
        return url

    def save(self, force_insert=False,
             force_update=False,
             commit=True):
        image = super().save(commit=False)  # создает экземпляр на основе данных из формы, но пока не сохраняет в БД
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'
        response = requests.get(image_url)  # скачиваем по url
        image.image.save(image_name,  # сохранение данного файла по указанному имени
                         ContentFile(response.content),
                         save=False)
        if commit:
            image.save()
        return image
