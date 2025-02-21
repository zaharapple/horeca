import redis
import json
from django.conf import settings


class Cart:
    EXPIRE_CART_TIME = 60 * 60 * 24

    def __init__(self, request):
        self.session = request.session
        self.redis = redis.Redis(host=settings.REDIS_BASE_URL, port=settings.REDIS_PORT, db=1)
        user_id = request.user.id if request.user.is_authenticated else request.session.session_key
        self.cart_key = f"cart:{user_id}"

        self.redis.expire(self.cart_key, self.EXPIRE_CART_TIME)

    def add(self, cart_data):
        cart_db = self.redis.hget(self.cart_key, cart_data.id)

        if cart_db:
            cart_item = json.loads(cart_db)
            cart_item["quantity"] += cart_data.quantity
        else:
            cart_item = {
                "id": cart_data.id,
                "name": cart_data.name,
                "size": cart_data.variant['id'],
                "ingredients": 'sss',
                "quantity": cart_data.quantity,
                "price": float(cart_data.price),
                "total_price": f"{float(cart_data.price * cart_data.quantity):.2f}",
            }

        self.redis.hset(self.cart_key, cart_data.id, json.dumps(cart_item))

    def remove(self, product_id):
        self.redis.hdel(self.cart_key, product_id)

    def get_items(self):
        cart_data = self.redis.hgetall(self.cart_key)
        items = [json.loads(value) for value in cart_data.values()]
        return items

    def clear(self):
        self.redis.delete(self.cart_key)
