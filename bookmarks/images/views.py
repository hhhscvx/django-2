from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action


@login_required
def image_create(request):
    if request.method == 'POST':  # форма отправлена
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            create_action(request.user, 'сохранил картинку', new_image)
            messages.success(request, 'Картинка успешно добавлена')
            return redirect(new_image.get_absolute_url())  # Перенаправляем на страницу загруженной только что картинки.
    else:  # форма получена и еще не заполнена вроде
        form = ImageCreateForm(data=request.GET)
    return render(request,
                  'images/image/create.html',
                  {'section': 'images',
                   'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request,
                  'images/image/detail.html',
                  {'section': 'images',  # section используется для разделения, типо dashboard/images/profiles
                   'image': image})


@login_required  # аутентифицирован
@require_POST  # запрос на POST (нажал кнопку like/unlike)
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')  # like/unlike
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)  # если поставил лайк - добавляется в список лайкнувших
                create_action(request.user, 'лайкнул', image)
            else:
                image.users_like.remove(request.user)  # не стоит лайк - удаляется из списка лайкнувших
            return JsonResponse({'status': 'ok'})  # возвращаем JSON со статусом что все успешно
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})  # возвращаем JSON со статусом что все плохо


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)  # картинки разбиваются на страницы по 8 картинок на каждой
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)  # если страница не целое число, вернуть первую страницу
    except EmptyPage:
        if images_only:
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)  # если такой страницы нет то выдать последнюю
    if images_only:
        return render(request,
                      'images/image/list_images.html',  # изображения только запрошенной страницы
                      {'section': 'images',
                       'images': images})

    return render(request,
                  'images/image/list.html',  # все изображения
                  {'section': 'images',
                   'images': images})
