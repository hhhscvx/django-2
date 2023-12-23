from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required  # для просмотра страницы, пользователь должен быть аунтефицирован, иначе будет направлен для авторизации
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])  # Задаем пароль через указанный в форме пароль
            new_user.save()  # сохраняем
            Profile.objects.create(user=new_user)  # При регистрации создаем профиль пользователя
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required  # только аутентифицированные пользователи могут редачить профиль
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,  # связывает форму с текущим пользователем
                                 data=request.POST)  # предоставляет данные из POST запроса для формы
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       # связывает форму с профилем текущего пользователя
                                       data=request.POST,
                                       files=request.FILES)  # файлы для аватарок и прочего
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()  # сохранение
            messages.success(request, 'Профиль успешно обновлен!')
        else:
            messages.error(request, 'Форма заполнена некорректно')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                  'account/user/list.html',
                  {'section': 'people',
                   'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    return render(request,
                  'account/user/detail.html',
                  {'section': 'people',
                   'user': user})
