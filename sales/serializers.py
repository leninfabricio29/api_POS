from rest_framework import serializers
from .models import Sale, Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['sale']


from customers.models import Customer
from customers.serializers import CustomerSerializer

class SaleSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=False, allow_null=True, write_only=True)
    customer_data = CustomerSerializer(write_only=True, required=False)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    tax = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Sale
        fields = ['id','order','customer','customer_data','customer_name','subtotal','tax','total','payments','created_at']
        read_only_fields = ['id','created_at']

    def create(self, validated_data):
        from cash.models import CashSession, CashMovement
        from django.utils import timezone
        payments_data = validated_data.pop('payments', [])
        customer = validated_data.pop('customer', None)
        customer_data = validated_data.pop('customer_data', None)
        order = validated_data.get('order')

        # Registrar o buscar cliente
        customer_instance = None
        if customer_data:
            # Buscar por doc_id si existe, si no crear
            doc_id = customer_data.get('doc_id')
            if doc_id:
                customer_instance, created = Customer.objects.get_or_create(doc_id=doc_id, defaults=customer_data)
                if not created:
                    # Actualizar datos si ya existe
                    for k, v in customer_data.items():
                        setattr(customer_instance, k, v)
                    customer_instance.save()
            else:
                customer_instance = Customer.objects.create(**customer_data)
            validated_data['customer_name'] = customer_instance.name
        elif customer:
            customer_instance = customer
            validated_data['customer_name'] = customer_instance.name
        else:
            # Consumidor final
            validated_data['customer_name'] = validated_data.get('customer_name', 'Consumidor final')

        # Calcular subtotal, tax y total si no vienen
        if order:
            if 'subtotal' not in validated_data:
                validated_data['subtotal'] = sum([item.subtotal for item in order.items.all()])
            if 'tax' not in validated_data:
                validated_data['tax'] = 0
            if 'total' not in validated_data:
                validated_data['total'] = validated_data['subtotal'] + validated_data['tax']

        sale = Sale.objects.create(**validated_data)
        for p in payments_data:
            Payment.objects.create(sale=sale, **p)

        # Registrar movimiento de caja global del día
        today = timezone.now().date()
        session = CashSession.objects.filter(opened_at__date=today, closed_at__isnull=True).first()
        if session:
            total_pago = sum([float(p['amount']) for p in payments_data])
            CashMovement.objects.create(
                session=session,
                type=CashMovement.Type.INFLOW,
                amount=total_pago,
                description=f"Venta #{sale.id}"
            )
        return sale