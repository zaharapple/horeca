from django.db import models

from modules.channel.models import Channel
from modules.customer.models import Customer
from .choices import OrderStatus, OrderType, OrderAddressType


class Order(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    code = models.CharField(max_length=255, db_index=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=OrderStatus.choices,
        db_index=True,
    )
    type = models.CharField(
        max_length=50,
        choices=OrderType.choices,
        db_index=True,
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField()
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    class Meta:
        db_table = "order"


class OrderAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='address')
    type = models.CharField(
        max_length=50,
        choices=OrderAddressType.choices,
        db_index=True,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "order_address"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    sku = models.CharField(max_length=255)
    qty = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sku

    class Meta:
        db_table = "order_item"


class OrderItemVariant(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='variants')
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    class Meta:
        db_table = "order_item_variant"


class OrderItemAdditive(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='additives')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "order_item_additive"


class OrderPackage(models.Model):
    order_item_variant = models.ForeignKey(OrderItemVariant, on_delete=models.CASCADE, related_name='packages')
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "order_package"
