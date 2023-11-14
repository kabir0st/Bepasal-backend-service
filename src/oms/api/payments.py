from core.utils.viewsets import DefaultViewSet
from oms.models.payment import Payment
from rest_framework.permissions import IsAuthenticated

from .serializers.payments import PaymentSerializer


class PaymentAPI(DefaultViewSet):
    serializer_class = PaymentSerializer
    search_fields = []
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.filter().order_by('-id')
    http_method_names = ['GET']

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset(invoice_summary__user=self.request.user)
