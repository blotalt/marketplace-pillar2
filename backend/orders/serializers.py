from rest_framework import serializers
from .models import Order, OrderItem, Coupon, Invoice

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_type', 'value', 'min_purchase', 'max_discount', 'is_active']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_name', 'product_type',
            'unit_price_usd', 'quantity', 'subtotal_usd',
            'license_key', 'download_url'
        ]

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'issue_date', 'due_date',
            'company_name', 'company_tax_id', 'company_address', 'notes'
        ]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    invoice = InvoiceSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer_name', 'customer_email',
            'customer_country', 'shipping_address', 'currency', 'exchange_rate',
            'subtotal_usd', 'discount_usd', 'shipping_usd', 'tax_usd', 'total_usd',
            'total_in_currency', 'coupon_code', 'referral_code', 'payment_method',
            'payment_status', 'created_at', 'items', 'invoice'
        ]
