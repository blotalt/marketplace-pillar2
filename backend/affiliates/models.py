import uuid
from django.db import models
from orders.models import Order

class Affiliate(models.Model):
    user_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=50, unique=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=15.00) # e.g. 15%
    total_clicks = models.PositiveIntegerField(default=0)
    total_earnings_usd = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    balance_payable_usd = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} ({self.code}) - {self.commission_rate}%"

class AffiliateReferral(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('paid', 'Paid Out'),
    ]
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE, related_name='referrals')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    order_total_usd = models.DecimalField(max_digits=10, decimal_places=2)
    commission_amount_usd = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='approved')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ref #{self.id} for {self.affiliate.code} (${self.commission_amount_usd})"

class PayoutRecord(models.Model):
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE, related_name='payouts')
    amount_usd = models.DecimalField(max_digits=10, decimal_places=2)
    payout_method = models.CharField(max_length=50, default='PayPal / Wise')
    transaction_reference = models.CharField(max_length=100, default=uuid.uuid4)
    status = models.CharField(max_length=20, default='Completed')
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payout ${self.amount_usd} to {self.affiliate.code}"
