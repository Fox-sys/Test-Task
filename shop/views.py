import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
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

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['price'] = Cart(self.request).get_price() / 100
        return context_data


class ItemDetailView(generic.DetailView):
    model = db_models.Item
    template_name = 'shop/item_detail.html'

    def get_context_data(self, **kwargs):
        cart = Cart(self.request)
        context_data = super().get_context_data(**kwargs)
        context_data['price'] = cart.get_price() / 100
        return context_data


class CheckoutView(generic.TemplateView):
    template_name = 'shop/checkout.html'

    def get_context_data(self, **kwargs):
        cart = Cart(self.request)
        context_data = super().get_context_data(**kwargs)
        context_data['public_key'] = settings.STRIPE_PUBLIC_KEY
        context_data['price'] = cart.get_price() / 100
        context_data['tax'] = cart.count_tax() / 100
        return context_data


class PaymentView(APIView):
    def put(self, request):
        """Проверка промокода"""
        promocode = None
        promocode_get_serializer = serializers.PromocodeGetSerializer(request.data)
        code = promocode_get_serializer.instance.get('code')
        try:
            promocode = db_models.PromoCode.objects.get(code=code)
        except db_models.PromoCode.DoesNotExist:
            pass
        if promocode:
            return Response(serializers.PromocodeReturnSerializer(instance=promocode).data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """Получение payment intent"""
        cart = Cart(request)
        cart.cart['discount'] = request.data['discount'] * 100
        cart.save()

        payment_intent = stripe.PaymentIntent.create(
            amount=round(cart.get_total_price()),
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
            amount=item_add_serializer.instance.get('amount', 1),
            update_amount=item_add_serializer.instance.get('update_amount', False)
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

    def post(self, request):
        cart = Cart(request)
        cart.create_order()
        return Response({'items': self.get_serialized_cart(cart)})


class WebHook(APIView):
    @csrf_exempt
    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_KEY
            )
        except ValueError:
            # Invalid payload
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            # Invalid signature
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if event['type'] == 'charge.succeeded':
            cart = Cart(request)
            cart.clear()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)
