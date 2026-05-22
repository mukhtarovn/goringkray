from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def send_new_order_email(order):
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            ['gorniykray05@mail.ru'],
            fail_silently=True,  # 🔥 важно
        )
    except Exception as e:
        print("EMAIL ERROR:", e)


