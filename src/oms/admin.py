from django.contrib import admin

from oms.models import (Category, Product, ProductImage, ProductVariation,
                        ProductVariationImage, Order, OrderItem,
                        OrderItemStatus,
                        OrderStatus, VariationType, VariationOption)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductVariation)
admin.site.register(ProductVariationImage)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(VariationType)
admin.site.register(OrderItemStatus)
admin.site.register(OrderStatus)

admin.site.register(VariationOption)
