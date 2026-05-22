from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.decorators.http import require_POST
from authapp.models import ShopUser
from basketapp.models import Basket
from main.models import Product

@login_required
def basket(request):
    title = 'Корзина'
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category')
    content = {
        'title': title,
        'basket_items': basket_items
    }
    return render(request, 'basketapp/basket.html', content)

@login_required
def basket_add(request, pk):  #pk - Product
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()
    if not basket:
        basket = Basket(user=request.user, product=product)
    basket.quantity += 1
    basket.save()
    send_mail ('ДОБАВИЛИ В КОРЗИНУ', f'Клиент {request.user} добавил {basket.product}  - {basket.quantity} шт',
               'luchi_sveta@list.ru', ['luchi_sveta@list.ru', 'mukhtarov.n@gmail.com'],
               fail_silently=False, )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_remove(request, pk):  #pk - basket
    basket_record = Basket.objects.filter(pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket = Basket.objects.get(pk=int(pk))
        if quantity > 0:
            new_basket.quantity = quantity
            new_basket.save()
        else:
            new_basket.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        content = {
            'basket_items': basket_items
        }

        result = render_to_string('basketapp/inc/inc_basket.html', content)
        return JsonResponse({'result': result})

@require_POST
def update_quantity(request, pk):
    try:
        item = Basket.objects.get(pk=pk)
        quantity = int(request.POST.get('quantity', 0))

        if quantity <= 0:
            item.delete()
            return JsonResponse({'success': True, 'deleted': True})

        item.quantity = quantity
        item.save()

        return JsonResponse({
            'success': True,
            'item_total': item.product.price * item.quantity,
            'total_quantity': item.total_quantity,
            'total_cost': item.total_cost,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
