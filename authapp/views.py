import random

from django.conf import settings
from django.contrib import auth


from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser

def send_varification_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    subject = f'Активация пользователя {user.username}'
    message = f'Для подтверждения перейдите по ссылке\n {settings.DOMAIN_NAME}{verify_link}'

    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, "authapp/verification.html")
        else:
            print(f'error{email}')
            return request(request, 'authapp/verification.html')
    except Exception as e:
        print(e.args)
        return HttpResponseRedirect(reverse('main'))


def login(request):
    title = 'Лучи свеиа:вход в личный кабинет'
    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            send_mail ('Клиент вошел в ЛК', f'{request.user} вошел в личный кабинет',
                       'luchi_sveta@list.ru', ['luchi_sveta@list.ru', 'mukhtarov.n@gmail.com'],
                       fail_silently=False, )
            return render(request, 'main/index.html')
    content = {
        'title': title,
        'login_form': login_form}
    return render(request, 'authapp/login.html', content)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))

def register(request):
    title = 'Лучи света: Регистарция пользователя'
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()
    content = {
       'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', content)


def edit(request):
    title = 'Лучи света:Редактирование данных пользователя'
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
    content = {
        'title': title, 'edit_form': edit_form}

    return render(request, 'authapp/edit.html', content)

def anonym(request):
    username = f'Anonym{random.randint(1,100)}'
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    password = 'shopuser12345'
    if request.method == 'POST':
        if name is not None:
            if phone is not None:
                phone = 111111
                ShopUser.objects.create_user(first_name=name, address=address, phone=phone,
                                             username=username, password=password)
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return render(request, 'main/index.html')
    return render(request, 'authapp/anonym.html')
