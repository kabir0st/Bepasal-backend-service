from django_filters import FilterSet
from ecommerce.models import Review, Cart


class ReviewFilter(FilterSet):

    class Meta:
        model = Review
        exclude = ('images',)


class CartFilter(FilterSet):

    class Meta:
        model = Cart
        include = '__all__'
