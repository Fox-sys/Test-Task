from django.db import models

CURRENCY_RUB = 'usd'
CURRENCY_EUR = 'eur'


class Item(models.Model):
    name = models.CharField('Название', max_length=150)
    description = models.TextField('Описание')
    price = models.PositiveIntegerField('Цена')
    currency = models.CharField('Валюта', max_length=3, choices=[(CURRENCY_EUR, 'Евро'), (CURRENCY_RUB, 'Рубли')])

    def __str__(self):
        return f'[{self.id}]: {self.name}'

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Order(models.Model):
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True, blank=True)
    tax = models.ForeignKey('Tax', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'[{self.id}]: {self.order_items.count()}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'заказы'


class OrderItem(models.Model):
    item = models.ForeignKey('Item', verbose_name='Пердмет', related_name='order_items',  on_delete=models.CASCADE)
    order = models.ForeignKey('Order', verbose_name='Заказ', related_name='order_items', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Часть заказа'
        verbose_name_plural = 'Части заказа'


class Discount(models.Model):
    amount = models.PositiveIntegerField('Цена скидки')

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return str(self.amount)


class Tax(models.Model):
    amount = models.PositiveIntegerField('Цена налога')

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'

    def __str__(self):
        return str(self.amount)


class PromoCode(models.Model):
    code = models.CharField('Код', max_length=15)
    amount = models.PositiveIntegerField('Цена промокода')
    is_active = models.BooleanField('Активен')

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
