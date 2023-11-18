from django.contrib import admin

from oms.models import (Category, Item, ItemImage, ItemVariation,
                        ItemVariationImage, Order, OrderItem, OrderItemStatus,
                        OrderStatus, VariationType, VariationOption)

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(ItemImage)
admin.site.register(ItemVariation)
admin.site.register(ItemVariationImage)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(VariationType)
admin.site.register(OrderItemStatus)
admin.site.register(OrderStatus)

admin.site.register(VariationOption)
