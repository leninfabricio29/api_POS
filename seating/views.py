from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Area, Table
from .serializers import AreaSerializer, TableSerializer

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['area','status']
    search_fields = ['code']

    @action(detail=True, methods=['post'])
    def set_status(self, request, pk=None):
        table = self.get_object()
        status = request.data.get('status')
        table.status = status
        table.save()
        return Response(TableSerializer(table).data)