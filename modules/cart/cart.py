import json
from django.core.cache import caches


class Cart:
    EXPIRE_CART_TIME = 7 * 24 * 60 * 60

    def __init__(self, request):
        self.session = request.session
        self.cart_cache = caches["cart_cache"]
        user_id = request.user.id if request.user.is_authenticated else self.session.session_key
        self.cart_key = f"cart:{user_id}"

        self.cart_cache.touch(self.cart_key, self.EXPIRE_CART_TIME)

    def add(self, cart_data):
        cart = self._get_cart()

        exist_product = cart.get(str(cart_data['variant_id']))
        if exist_product:

            cart[str(cart_data['variant_id'])]["quantity"] += cart_data['quantity']  # TODO: If no same variants
        else:
            cart[cart_data['variant_id']] = cart_data

        self.cart_cache.set(self.cart_key, json.dumps(cart), timeout=self.EXPIRE_CART_TIME)

    def remove(self, product_id):
        cart = self._get_cart()
        if str(product_id) in cart:
            del cart[str(product_id)]
            self.cart_cache.set(self.cart_key, json.dumps(cart), timeout=self.EXPIRE_CART_TIME)

    def get_items(self):
        return list(self._get_cart().values())

    def clear(self):
        self.cart_cache.delete(self.cart_key)

    def _get_cart(self):
        cart_data = self.cart_cache.get(self.cart_key)
        return json.loads(cart_data) if cart_data else {}
