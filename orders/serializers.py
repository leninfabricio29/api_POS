# orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
from catalog.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    # Opción A: que NO se pueda enviar price desde el cliente (snapshot automático):
    # price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    # Opción B: permitir override opcional (descuentos/promos), si no viene lo calculamos:
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = OrderItem
        # Nota: NO incluimos 'order' aquí
        fields = ('id', 'product', 'quantity', 'note', 'price')
        read_only_fields = ('id',)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Order
        fields = ['id','table','customer','waiter','status','notes','items','created_at','updated_at','total']
        read_only_fields = ['id','created_at','updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)

        for item in items_data:
            product = item['product']              # ya es instancia por PKRelatedField
            qty = item.get('quantity', 1)
            # si no viene price, tomar snapshot desde el producto
            price = item.get('price', product.price)
            OrderItem.objects.create(
                order=order, product=product, quantity=qty, price=price, note=item.get('note')
            )
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        if items_data is not None:
            # Mapeo de productos existentes
            existing_items = {item.product_id: item for item in instance.items.all()}
            new_product_ids = set()
            for item in items_data:
                product = item['product']
                qty = item.get('quantity', 1)
                price = item.get('price', product.price)
                note = item.get('note')
                new_product_ids.add(product.id)
                if product.id in existing_items:
                    order_item = existing_items[product.id]
                    order_item.quantity = qty
                    order_item.price = price
                    order_item.note = note
                    order_item.save()
                else:
                    OrderItem.objects.create(
                        order=instance, product=product, quantity=qty, price=price, note=note
                    )
            # Eliminar productos que ya no están
            for pid, order_item in existing_items.items():
                if pid not in new_product_ids:
                    order_item.delete()
        return instance