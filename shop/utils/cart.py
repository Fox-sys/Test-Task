from django.conf import settings
from shop import models as db_models


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {'discount': 0}
        self.cart = cart

    def count_tax(self):
        return self.get_price() * settings.TAX_MULTIPLIER

    def get_total_price(self):
        return self.get_price() + self.count_tax() - self.cart['discount']

    def __iter__(self):
        cart = self.cart.copy()
        try:
            cart.pop('discount')
        except:
            pass

        for item in cart:
            yield item

    def keys(self):
        return self.cart.keys()

    def __len__(self):
        return sum(item['amount'] for item in self.cart.values())

    def add(self, item: db_models.Item, amount=1, update_amount=False):
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {
                'amount': 0
            }
        if update_amount:
            self.cart[item_id]['amount'] = amount
        else:
            self.cart[item_id]['amount'] += amount
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, item: db_models.Item):
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def get_price(self):
        items = self.get_in_cart_items()
        return sum([item.price * self.cart[str(item.id)]['amount'] for item in items])

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.cart = {}
        self.save()

    def get_in_cart_items(self):
        keys = list(self.cart.keys())
        keys.remove('discount')
        item_ids = keys
        return db_models.Item.objects.filter(id__in=item_ids)

    def create_order(self):
        order = db_models.Order.objects.create()
        for item_id in self:
            item = db_models.Item.objects.get(id=int(item_id))
            new_item = db_models.OrderItem.objects.create(
                order=order,
                item=item,
                amount=self.cart[item_id]['amount']
            )
            new_item.save()
        order.discount = db_models.Discount.objects.create(amount=self.cart['discount'])
        order.tax = db_models.Tax.objects.create(amount=self.count_tax())
        order.save()
        self.discount = 0
        self.clear()
