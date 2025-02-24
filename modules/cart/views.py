from decimal import Decimal
from typing import Dict

from pydantic import BaseModel, conint, condecimal
from django.http import JsonResponse
from django.views import View

from modules.product.models import Product, ProductVariant, Additive
from .cart import Cart
from dataclasses import dataclass


class CartData(BaseModel):
    id: int
    name: str
    variant: Dict
    additives: Dict
    additive_total: Decimal
    quantity: conint(ge=1)
    price: condecimal(max_digits=10, decimal_places=2)

    def to_dict(self):
        total_price = self.price * self.quantity + self.additive_total

        return {
            "variant_id": self.id,
            "name": self.name,
            "variant": self.variant,
            "additives": self.additives,
            "quantity": self.quantity,
            "price": float(self.price),
            "total_price": float(total_price),
        }


class CartView(View):

    def get(self, request):
        cart = Cart(request)
        return JsonResponse({"cart": cart.get_items()})


class AddToCartView(View):

    def post(self, request, product_id):
        cart = Cart(request)
        variant_id = request.POST.get("variant_id")
        additive_ids = request.POST.get("additive_ids", "")

        if not variant_id:
            return JsonResponse({"error": "Variant ID is required"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
            variant = ProductVariant.objects.get(id=variant_id, product=product)

            if additive_ids:
                additive_ids_list = [int(i) for i in additive_ids.split(",") if i.isdigit()]
                additives = Additive.objects.filter(id__in=additive_ids_list)
            else:
                additives = []

            additives_total = Decimal("0")
            additives_data = {}

            for additive in additives:
                additives_data[additive.name] = {
                    'id': additive.id,
                    'price': float(additive.price),
                    'image': additive.image.url
                }
                additives_total += additive.price

            cart_data = CartData(
                id=product.id,
                name=product.name,
                variant={
                    'name': variant.name,
                    'id': variant_id
                },
                additives=additives_data,
                additive_total=additives_total,
                quantity=int(request.POST.get("quantity", 1)),
                price=variant.price,
            )

            cart.add(cart_data.to_dict())
            return JsonResponse({"message": "Product added to cart", "cart": cart.get_items()})
        except (Product.DoesNotExist, ProductVariant.DoesNotExist):
            return JsonResponse({"error": "Invalid product or variant"}, status=400)


class RemoveFromCartView(View):

    def post(self, request, product_id):
        cart = Cart(request)
        cart.remove(product_id)
        return JsonResponse({"message": "Product removed from cart", "cart": cart.get_items()})


class ClearCartView(View):

    def post(self, request):
        cart = Cart(request)
        cart.clear()
        return JsonResponse({"message": "Cart cleared"})
