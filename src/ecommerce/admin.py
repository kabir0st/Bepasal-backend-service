from django.contrib import admin

from ecommerce.models.ecom import Cart, CartItem, Review, ReviewImage

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Review)
admin.site.register(ReviewImage)
