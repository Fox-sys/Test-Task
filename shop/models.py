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
    items = models.ManyToManyField('Item', verbose_name='Предметы')
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'[{self.id}]: {self.items.count()}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'заказы'


class Discount(models.Model):
    pass

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'
