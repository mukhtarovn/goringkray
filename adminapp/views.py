from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render

from main.models import ProductCategory, Product

@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    content = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', content)


def user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm (request.POST, request.FILES)
        if user_form.is_valid ():
            user_form.save ()
            return HttpResponseRedirect (reverse ('admin:users'))
    else:
        user_form = ShopUserRegisterForm ()

    content = {'title': title, 'update_form': user_form}

    return render (request, 'adminapp/user_update.html', content)


class ShopUserAdminEditForm (object):
    pass


def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404 (ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm (request.POST, request.FILES, \
                                           instance=edit_user)
        if edit_form.is_valid ():
            edit_form.save ()
            return HttpResponseRedirect (reverse ('admin:user_update', \
                                                  args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm (instance=edit_user)

    content = {'title': title, 'update_form': edit_form}

    return render (request, 'adminapp/user_update.html', content)


def user_delete(request, pk):
    title = 'пользователи/удаление'

    user = get_object_or_404 (ShopUser, pk=pk)

    if request.method == 'POST':
        # user.delete()
        # вместо удаления лучше сделаем неактивным
        user.is_active = False
        user.save ()
        return HttpResponseRedirect (reverse ('admin:users'))

    content = {'title': title, 'user_to_delete': user}

    return render (request, 'adminapp/user_delete.html', content)


def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    content = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', content)


def category_create(request):
    pass


def category_update(request, pk):
    pass


def category_delete(request, pk):
    pass


def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    content = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', content)


def product_create(request, pk):
    pass


def product_read(request, pk):
    pass


def product_update(request, pk):
    pass


def product_delete(request, pk):
    pass

