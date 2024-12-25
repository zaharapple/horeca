from django.db import models

from ..base.models import TimeStampeMixin
from ..channel.models import Channel
from ..customer.models import Customer


class Order(models.Model, TimeStampeMixin):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    code = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField()

    def __str__(self):
        return self.code

    class Meta:
        db_table = "order"


class OrderAddress(models.Model, TimeStampeMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='address')
    type = models.CharField(max_length=50)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)

    class Meta:
        db_table = "order_address"


class OrderItem(models.Model, TimeStampeMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    sku = models.CharField(max_length=255)
    qty = models.IntegerField()

    def __str__(self):
        return self.sku

    class Meta:
        db_table = "order_item"


class OrderItemVariant(models.Model, TimeStampeMixin):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='variants')
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.code

    class Meta:
        db_table = "order_item_variant"


class OrderItemAdditive(models.Model, TimeStampeMixin):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='additives')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "order_item_additive"


class OrderPackage(models.Model, TimeStampeMixin):
    order_item_variant = models.ForeignKey(OrderItemVariant, on_delete=models.CASCADE, related_name='packages')
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "order_package"
