from django.db import models


class OrderType(models.TextChoices):
    online = 'online', 'Online'
    offline = 'offline', 'Offline'


class OrderStatus(models.TextChoices):
    pending_payment = 'pending_payment', 'Pending Payment'
    processing = 'processing', 'Processing'
    complete = 'complete', 'Complete'
    closed = 'closed', 'Closed'
    delivered = 'delivered', 'Delivered'

    canceled = 'canceled', 'Canceled'
    not_delivered = 'not_delivered', 'Not Delivered'


class OrderAddressType(models.TextChoices):
    billing = 'billing', 'Billing'
    shipping = 'shipping', 'Shipping'

