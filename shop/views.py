import stripe
from rest_framework.response import Response

from . import models as db_models
from django.views.generic import DetailView, ListView
from rest_framework.views import APIView
from . import serializers
from .utils.cart import Cart


class ItemListView(ListView):
    model = db_models.Item
    template_name = 'shop/item_list.html'


class ItemDetailView(DetailView):
    model = db_models.Item
    template_name = 'shop/item_detail.html'


class CreatePaymentIntentView(APIView):
    def post(self, request):
        item_list_serializer = serializers.ItemListSerializer(request.data)
        item_ids: list[int] = item_list_serializer.instance.get('item_ids')
        items = db_models.Item.objects.filter(id__in=item_ids)
        order = db_models.Order.objects.create()
        order.items.add(*items)
        order.save()

        payment_intent = stripe.PaymentIntent.create(
            amount=order.get_price(),
            currency='usd',
            automatic_payment_methods={
                'enabled': True
            }
        )
        return Response({'client_secret': payment_intent.client_secret})


class CartView(APIView):
    def get_serialized_cart(self, cart):
        items = []
        for item_id in cart.keys():
            items.append(
                {
                    'amount': cart.cart[item_id]['amount'],
                    'item': serializers.ItemSerializer(db_models.Item.objects.get(id=item_id)).data
                 }
            )
        return items

    def get(self, request):
        cart = Cart(request)
        return Response({'items': self.get_serialized_cart(cart)})

    def put(self, request):
        cart = Cart(request)
        item_add_serializer = serializers.CartItemAddSerializer(request.data)
        item = db_models.Item.objects.get(id=item_add_serializer.instance.get('item_id'))
        cart.add(
            item,
            amount=item_add_serializer.instance.get('amount'),
            update_amount=item_add_serializer.instance.get('update_amount')
        )
        items = self.get_serialized_cart(cart)
        return Response({'items': items})

    def patch(self, request):
        cart = Cart(request)
        item_remove_serializer = serializers.CartItemRemoveSerializer(request.data)
        item = db_models.Item.objects.get(id=item_remove_serializer.instance.get('item_id'))
        cart.remove(item)
        items = self.get_serialized_cart(cart)
        return Response({'items': items})

    def delete(self, request):
        cart = Cart(request)
        cart.clear()
        return Response({'items': self.get_serialized_cart(cart)})
