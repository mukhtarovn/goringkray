from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from basketapp.models import Basket
from main.models import Product


def get_session_key(request):
    """
    Создаёт session_key для гостя, если его ещё нет.
    """
    if not request.session.session_key:
        request.session.save()

    return request.session.session_key


def get_basket_items(request):
    """
    Возвращает корзину текущего пользователя или гостя.
    """
    if request.user.is_authenticated:
        return Basket.get_items(user=request.user)

    session_key = get_session_key(request)

    return Basket.get_items(session_key=session_key)


def get_basket_item(request, pk):
    """
    Получаем только тот товар корзины,
    который принадлежит текущему пользователю или текущей сессии.
    """
    if request.user.is_authenticated:
        return get_object_or_404(
            Basket,
            pk=pk,
            user=request.user
        )

    session_key = get_session_key(request)

    return get_object_or_404(
        Basket,
        pk=pk,
        session_key=session_key
    )


def basket(request):
    title = 'Корзина'

    basket_items = get_basket_items(request)

    content = {
        'title': title,
        'basket_items': basket_items
    }

    return render(
        request,
        'basketapp/basket.html',
        content
    )


def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user.is_authenticated:

        basket = Basket.objects.filter(
            user=request.user,
            product=product
        ).first()

        if not basket:
            basket = Basket(
                user=request.user,
                product=product,
                quantity=0
            )

    else:

        session_key = get_session_key(request)

        basket = Basket.objects.filter(
            session_key=session_key,
            product=product
        ).first()

        if not basket:
            basket = Basket(
                session_key=session_key,
                product=product,
                quantity=0
            )

    basket.quantity += 1
    basket.save()

    try:
        send_mail(
            'ДОБАВИЛИ В КОРЗИНУ',
            f'Клиент добавил {basket.product} - {basket.quantity} шт',
            'luchi_sveta@list.ru',
            [
                'luchi_sveta@list.ru',
                'mukhtarov.n@gmail.com'
            ],
            fail_silently=False,
        )
    except Exception:
        pass

    return HttpResponseRedirect(
        request.META.get('HTTP_REFERER', '/')
    )


def basket_remove(request, pk):
    basket_record = get_basket_item(request, pk)

    basket_record.delete()

    return HttpResponseRedirect(
        request.META.get('HTTP_REFERER', '/')
    )


def basket_edit(request, pk, quantity):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        quantity = int(quantity)

        new_basket = get_basket_item(request, pk)

        if quantity > 0:
            new_basket.quantity = quantity
            new_basket.save()
        else:
            new_basket.delete()

        basket_items = get_basket_items(request)

        content = {
            'basket_items': basket_items
        }

        result = render_to_string(
            'basketapp/inc/inc_basket.html',
            content,
            request=request
        )

        return JsonResponse({
            'result': result
        })

    return JsonResponse({
        'success': False,
        'error': 'Invalid request'
    })


@require_POST
def update_quantity(request, pk):

    try:
        item = get_basket_item(request, pk)

        quantity = int(
            request.POST.get('quantity', 0)
        )

        if quantity <= 0:
            item.delete()

            basket_items = get_basket_items(request)

            total_quantity = sum(
                x.quantity for x in basket_items
            )

            total_cost = sum(
                x.product_cost for x in basket_items
            )

            return JsonResponse({
                'success': True,
                'deleted': True,
                'total_quantity': total_quantity,
                'total_cost': total_cost,
            })

        item.quantity = quantity
        item.save()

        basket_items = get_basket_items(request)

        total_quantity = sum(
            x.quantity for x in basket_items
        )

        total_cost = sum(
            x.product_cost for x in basket_items
        )

        return JsonResponse({
            'success': True,
            'item_total': item.product.price * item.quantity,
            'total_quantity': total_quantity,
            'total_cost': total_cost,
        })

    except (ValueError, TypeError):
        return JsonResponse({
            'success': False,
            'error': 'Некорректное количество'
        })

    except Basket.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Товар корзины не найден'
        })