from django.contrib import admin

from ecommerce.models.ecom import (
    QA, Cart,  Review, ReviewImage, WishList)

# Register your models here.
admin.site.register(Cart)
admin.site.register(Review)
admin.site.register(ReviewImage)
admin.site.register(QA)
admin.site.register(WishList)
