from core.utils.viewsets import DefaultViewSet
from oms.api.serializers.order import OrderSerializer
from oms.models.order import Order


class OrderAPI(DefaultViewSet):
    serializer_class = OrderSerializer
    search_fields = ['user_name', 'user_contact']
    queryset = Order.objects.filter().order_by('-id')
