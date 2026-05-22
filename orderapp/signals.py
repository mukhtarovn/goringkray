from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order
from .utils import send_new_order_email


@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        send_new_order_email(instance)
