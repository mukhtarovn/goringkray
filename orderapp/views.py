from django.core.mail import send_mail
from django.db import transaction
from django.forms import inlineformset_factory, formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView

from authapp.models import ShopUser
from basketapp.models import Basket
from orderapp.forms import OrderItemForm
from orderapp.models import Order, OrderItem


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orderapp:order_list')


    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        OrderFormSet= inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        # OrderFormSet=formset_factory(OrderItem)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.get_items(self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory (Order, OrderItem,
                                                      form=OrderItemForm, extra=len (basket_items))
                formset = OrderFormSet()
                for num, form in enumerate (formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price

                # basket_items.delete ()
            else:
                formset = OrderFormSet()
        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data ()
        orderitems = context['orderitems']

        with transaction.atomic ():
            Basket.get_items(self.request.user).delete()
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            if self.object.get_total_cost() == 0:
                self.object.delete()

            return super(OrderItemsCreate, self).form_valid(form)


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orderapp:order_list')


    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdate, self).get_context_data(**kwargs)
        OrderFormSet= inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
               if form.instance.pk:
                   form.initial['price'] = form.instance.product.price

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data ()
        orderitems = context['orderitems']

        self.object = form.save()
        if orderitems.is_valid():
            orderitems.instance = self.object
            orderitems.save()
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsUpdate, self).form_valid(form)

class OrderDelete(DeleteView):
   model = Order
   success_url = reverse_lazy('orderapp:order_list')

class OrderRead(DetailView):
   model = Order

   def get_context_data(self, **kwargs):
       context = super(OrderRead, self).get_context_data(**kwargs)
       context['title'] = 'заказ/просмотр'
       return context

def order_forming_complete(request, pk):
   order = get_object_or_404(Order, pk=pk)
   order.status = Order.SENT_TO_PROCEED
   order.save()
   send_mail('НОВЫЙ ЗАКАЗ', f'Поступил новый заказ {order.id} от {request.user}',
             'luchi_sveta@list.ru', ['luchi_sveta@list.ru', 'mukhtarov.n@gmail.com'],
             fail_silently=False,)

   return HttpResponseRedirect(reverse('orderapp:order_list'))