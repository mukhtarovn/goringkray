from django.core.mail import send_mail
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView
)

from basketapp.models import Basket
from orderapp.forms import OrderItemForm
from orderapp.models import Order, OrderItem


def get_session_key(request):
    """
    Создаём session_key для гостя.
    """
    if not request.session.session_key:
        request.session.save()

    return request.session.session_key


def get_order_items(request):
    """
    Получаем корзину текущего пользователя или гостя.
    """
    if request.user.is_authenticated:
        return Basket.get_items(user=request.user)

    session_key = get_session_key(request)

    return Basket.get_items(session_key=session_key)


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(
                user=self.request.user
            ).order_by('-created')

        session_key = self.request.session.session_key

        if not session_key:
            return Order.objects.none()

        return Order.objects.filter(
            session_key=session_key
        ).order_by('-created')


class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orderapp:order_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        OrderFormSet = inlineformset_factory(
            Order,
            OrderItem,
            form=OrderItemForm,
            extra=1
        )

        if self.request.POST:

            formset = OrderFormSet(
                self.request.POST
            )

        else:

            basket_items = get_order_items(self.request)

            OrderFormSet = inlineformset_factory(
                Order,
                OrderItem,
                form=OrderItemForm,
                extra=len(basket_items)
            )

            formset = OrderFormSet()

            for num, form in enumerate(formset.forms):

                if num >= len(basket_items):
                    break

                form.initial['product'] = basket_items[num].product
                form.initial['quantity'] = basket_items[num].quantity
                form.initial['price'] = basket_items[num].product.price

        data['orderitems'] = formset

        return data

    def form_valid(self, form):

        context = self.get_context_data()
        orderitems = context['orderitems']

        if not orderitems.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form)
            )

        basket_items = get_order_items(self.request)

        if not basket_items.exists():
            return self.render_to_response(
                self.get_context_data(form=form)
            )

        with transaction.atomic():

            # Сначала создаём заказ
            form.instance.user = (
                self.request.user
                if self.request.user.is_authenticated
                else None
            )

            # Для гостя сохраняем session_key
            if self.request.user.is_authenticated:
                form.instance.session_key = None
            else:
                form.instance.session_key = get_session_key(
                    self.request
                )

            self.object = form.save()

            # Сохраняем товары заказа
            orderitems.instance = self.object
            orderitems.save()

            # Проверяем сумму
            if self.object.get_total_cost() == 0:
                self.object.delete()

                return self.render_to_response(
                    self.get_context_data(form=form)
                )

            # Только после успешного создания заказа
            # удаляем корзину
            basket_items.delete()

        return HttpResponseRedirect(
            self.get_success_url()
        )


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orderapp:order_list')

    def get_context_data(self, **kwargs):

        data = super().get_context_data(**kwargs)

        OrderFormSet = inlineformset_factory(
            Order,
            OrderItem,
            form=OrderItemForm,
            extra=1
        )

        if self.request.POST:

            formset = OrderFormSet(
                self.request.POST,
                instance=self.object
            )

        else:

            formset = OrderFormSet(
                instance=self.object
            )

            for form in formset.forms:

                if form.instance.pk:
                    form.initial['price'] = (
                        form.instance.product.price
                    )

        data['orderitems'] = formset

        return data

    def form_valid(self, form):

        context = self.get_context_data()
        orderitems = context['orderitems']

        if orderitems.is_valid():

            self.object = form.save()

            orderitems.instance = self.object
            orderitems.save()

            if self.object.get_total_cost() == 0:
                self.object.delete()

            return HttpResponseRedirect(
                self.get_success_url()
            )

        return self.render_to_response(
            self.get_context_data(form=form)
        )


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orderapp:order_list')


class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['title'] = 'заказ/просмотр'

        return context


def order_forming_complete(request, pk):

    order = get_object_or_404(
        Order,
        pk=pk
    )

    order.status = Order.SENT_TO_PROCEED
    order.save()

    send_mail(
        'НОВЫЙ ЗАКАЗ',
        f'Поступил новый заказ {order.id}',
        'luchi_sveta@list.ru',
        [
            'luchi_sveta@list.ru',
            'mukhtarov.n@gmail.com'
        ],
        fail_silently=False,
    )

    return HttpResponseRedirect(
        reverse('orderapp:order_list')
    )