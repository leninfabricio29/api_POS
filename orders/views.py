from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('table','customer','waiter').prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status','table']

    @action(detail=True, methods=['post'])
    def send_to_kitchen(self, request, pk=None):
        order = self.get_object()
        order.status = Order.Status.SENT
        order.save()
        return Response(self.get_serializer(order).data)

    @action(detail=True, methods=['post'])
    def mark_ready(self, request, pk=None):
        order = self.get_object()
        order.status = Order.Status.READY
        order.save()
        return Response(self.get_serializer(order).data)

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        order = self.get_object()
        order.status = Order.Status.CLOSED
        order.save()
        return Response(self.get_serializer(order).data)

    @action(detail=True, methods=['get'])
    def ticket(self, request, pk=None):
        order = self.get_object()
        # Estructura simple de ticket de pedido
        data = {
            'pedido_id': order.id,
            'mesa': order.table.code if order.table else None,
            'cliente': order.customer.name if order.customer else 'Consumidor final',
            'mozo': order.waiter.username if order.waiter else None,
            'estado': order.get_status_display(),
            'items': [
                {
                    'producto': item.product.name,
                    'cantidad': item.quantity,
                    'precio': float(item.price),
                    'subtotal': float(item.subtotal),
                    'nota': item.note
                } for item in order.items.all()
            ],
            'total': float(order.total),
            'notas': order.notes,
            'fecha': order.created_at,
        }
        return Response(data)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related('order','product')
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]