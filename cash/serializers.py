from rest_framework import serializers
from .models import CashSession, CashMovement

class CashMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashMovement
        fields = '__all__'

class CashSessionSerializer(serializers.ModelSerializer):
    movements = CashMovementSerializer(many=True, read_only=True)

    class Meta:
        model = CashSession
        fields = ['id','user','opened_at','opening_amount','closed_at','closing_amount','notes','movements','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']