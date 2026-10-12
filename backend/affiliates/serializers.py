from rest_framework import serializers
from .models import Affiliate, AffiliateReferral, PayoutRecord

class AffiliateReferralSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)

    class Meta:
        model = AffiliateReferral
        fields = ['id', 'order_number', 'order_total_usd', 'commission_amount_usd', 'status', 'created_at']

class PayoutRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayoutRecord
        fields = ['id', 'amount_usd', 'payout_method', 'transaction_reference', 'status', 'paid_at']

class AffiliateSerializer(serializers.ModelSerializer):
    referrals = AffiliateReferralSerializer(many=True, read_only=True)
    payouts = PayoutRecordSerializer(many=True, read_only=True)
    total_sales_count = serializers.SerializerMethodField()
    conversion_rate = serializers.SerializerMethodField()

    class Meta:
        model = Affiliate
        fields = [
            'id', 'user_name', 'email', 'code', 'commission_rate',
            'total_clicks', 'total_earnings_usd', 'balance_payable_usd',
            'total_sales_count', 'conversion_rate', 'created_at',
            'referrals', 'payouts'
        ]

    def get_total_sales_count(self, obj):
        return obj.referrals.count()

    def get_conversion_rate(self, obj):
        if obj.total_clicks == 0:
            return 0.0
        return round((obj.referrals.count() / obj.total_clicks) * 100, 2)
