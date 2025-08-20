from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CashSession, CashMovement
from .serializers import CashSessionSerializer, CashMovementSerializer

class CashSessionViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        session = self.get_object()
        ingresos = sum([m.amount for m in session.movements.filter(type='INFLOW')])
        egresos = sum([m.amount for m in session.movements.filter(type='OUTFLOW')])
        saldo = float(session.opening_amount) + float(ingresos) - float(egresos)
        data = {
            'caja_id': session.id,
            'abierta': session.is_open,
            'monto_inicial': float(session.opening_amount),
            'ingresos': float(ingresos),
            'egresos': float(egresos),
            'saldo_actual': saldo,
            'fecha_apertura': session.opened_at,
            'fecha_cierre': session.closed_at,
            'notas': session.notes,
        }
        return Response(data)
    queryset = CashSession.objects.prefetch_related('movements')
    serializer_class = CashSessionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        from django.utils import timezone
        session = self.get_object()
        session.closed_at = timezone.now()
        session.closing_amount = request.data.get('closing_amount', session.closing_amount)
        session.save()
        return Response(self.get_serializer(session).data)

class CashMovementViewSet(viewsets.ModelViewSet):
    queryset = CashMovement.objects.select_related('session')
    serializer_class = CashMovementSerializer
    permission_classes = [IsAuthenticated]