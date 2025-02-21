from decimal import Decimal
from typing import Dict

from django.http import JsonResponse
from django.views import View
from modules.product.models import Product, ProductVariant, Additive
from .cart import Cart
from dataclasses import dataclass


@dataclass
class CartData:
    id: int
    name: str
    variant: Dict
    additives: Dict
    quantity: int
    price: Decimal


class CartView(View):

    def get(self, request):
        cart = Cart(request)
        return JsonResponse({"cart": cart.get_items()})


class AddToCartView(View):

    def post(self, request, product_id):
        cart = Cart(request)
        variant_id = request.POST.get("variant_id")
        ingredient_ids = request.POST.get("ingredient_ids", "")

        if not variant_id:
            return JsonResponse({"error": "Variant ID is required"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
            variant = ProductVariant.objects.get(id=variant_id, product=product)

            if ingredient_ids:
                ingredient_ids_list = [int(i) for i in ingredient_ids.split(",") if i.isdigit()]
                ingredients = Additive.objects.filter(id__in=ingredient_ids_list)
            else:
                ingredients = []

            cart_data = CartData(
                id=product.id,
                name=product.name,
                variant={
                    'name': variant.name,
                    'id': variant_id
                },
                additives={
                    additive.name: {
                        'id': additive.id,
                        'price': additive.price,
                        'image': additive.image.url
                    } for additive in ingredients
                },
                quantity=int(request.POST.get("quantity", 1)),
                price=variant.price,
            )

            cart.add(cart_data)
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
