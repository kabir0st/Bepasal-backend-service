from django.contrib import admin

from ecommerce.models.ecom import (
    QA, Cart, CartItem, Review, ReviewImage, WishList)

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Review)
admin.site.register(ReviewImage)
admin.site.register(QA)
admin.site.register(WishList)
