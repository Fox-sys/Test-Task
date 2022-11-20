import stripe
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from django.views import generic

from . import models as db_models
from . import serializers

from .utils.cart import Cart


class ItemListView(generic.ListView):
    model = db_models.Item
    template_name = 'shop/item_list.html'


class ItemDetailView(generic.DetailView):
    model = db_models.Item
    template_name = 'shop/item_detail.html'


class CheckoutView(generic.TemplateView):
    template_name = 'shop/checkout.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['public_key'] = settings.STRIPE_PUBLIC_KEY
        context_data['price'] = Cart(self.request).get_total_price() / 100
        return context_data


class CreatePaymentIntentView(APIView):
    def post(self, request):
        cart = Cart(request)

        payment_intent = stripe.PaymentIntent.create(
            amount=cart.get_total_price(),
            currency='usd',
        )
        return Response({'clientSecret': payment_intent.client_secret})


class CartView(APIView):
    def get_serialized_cart(self, cart):
        items = []
        for item_id in cart:
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
