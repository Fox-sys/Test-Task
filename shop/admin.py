from django.contrib import admin
from . import models as db_models


class OrderItemInline(admin.StackedInline):
    model = db_models.OrderItem
    extra = 1


@admin.register(db_models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'name', 'price')
    search_fields = ('id', 'name')


@admin.register(db_models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'discount', 'tax')
    inlines = [OrderItemInline]


@admin.register(db_models.PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'amount', 'is_active']
