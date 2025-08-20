from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Sale, Payment
from rest_framework.decorators import action
from .serializers import SaleSerializer, PaymentSerializer
from rest_framework.response import Response

class SaleViewSet(viewsets.ModelViewSet):
    from orders.models import Order
    @action(detail=True, methods=['get'])
    def ticket(self, request, pk=None):
        sale = self.get_object()
        order = sale.order
        data = {
            'venta_id': sale.id,
            'pedido_id': order.id if order else None,
            'cliente': sale.customer_name or (order.customer.name if order and order.customer else 'Consumidor final'),
            'items': [
                {
                    'producto': item.product.name,
                    'cantidad': item.quantity,
                    'precio': float(item.price),
                    'subtotal': float(item.subtotal),
                    'nota': item.note
                } for item in order.items.all()
            ] if order else [],
            'subtotal': float(sale.subtotal),
            'impuesto': float(sale.tax),
            'total': float(sale.total),
            'pagos': [
                {
                    'metodo': p.method,
                    'monto': float(p.amount),
                    'referencia': p.reference
                } for p in sale.payments.all()
            ],
            'fecha': sale.created_at,
        }
        return Response(data)
    queryset = Sale.objects.select_related('order').prefetch_related('payments')
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('sale')
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]