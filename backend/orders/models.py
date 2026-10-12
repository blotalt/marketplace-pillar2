import uuid
from django.db import models
from django.utils import timezone
from products.models import Product

class DiscountType(models.TextChoices):
    PERCENT = 'PERCENT', 'Percentage'
    FIXED = 'FIXED', 'Fixed Amount (USD)'

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices, default=DiscountType.PERCENT)
    value = models.DecimalField(max_digits=8, decimal_places=2, help_text="Percentage (e.g. 20) or fixed USD amount")
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    usage_count = models.PositiveIntegerField(default=0)
    max_uses = models.PositiveIntegerField(null=True, blank=True)

    def is_valid_for(self, subtotal):
        if not self.is_active:
            return False, "This promo code is no longer active."
        if self.valid_until and self.valid_until < timezone.now():
            return False, "This promo code has expired."
        if self.max_uses and self.usage_count >= self.max_uses:
            return False, "This promo code has reached its maximum redemptions."
        if subtotal < float(self.min_purchase):
            return False, f"Minimum purchase of ${self.min_purchase:.2f} required for this coupon."
        return True, "Valid coupon applied!"

    def calculate_discount(self, subtotal):
        subtotal = float(subtotal)
        if self.discount_type == DiscountType.PERCENT:
            discount = (float(self.value) / 100.0) * subtotal
        else:
            discount = min(float(self.value), subtotal)
        
        if self.max_discount:
            discount = min(discount, float(self.max_discount))
        return round(discount, 2)

    def __str__(self):
        return f"{self.code} ({self.value}{'%' if self.discount_type == DiscountType.PERCENT else ' USD'})"

class Order(models.Model):
    order_number = models.CharField(max_length=36, unique=True, default=uuid.uuid4)
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_country = models.CharField(max_length=100, default='United States')
    shipping_address = models.TextField(blank=True, default='')
    
    # Currency details
    currency = models.CharField(max_length=10, default='USD')
    exchange_rate = models.DecimalField(max_digits=12, decimal_places=6, default=1.0)
    
    # Financial breakdown in USD base
    subtotal_usd = models.DecimalField(max_digits=10, decimal_places=2)
    discount_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_usd = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Converted final amount in customer chosen currency
    total_in_currency = models.DecimalField(max_digits=16, decimal_places=4)
    
    coupon_code = models.CharField(max_length=50, blank=True, default='')
    referral_code = models.CharField(max_length=50, blank=True, default='')
    
    payment_method = models.CharField(max_length=50, default='Credit Card')
    payment_status = models.CharField(max_length=20, default='PAID') # PAID, PENDING, REFUNDED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.order_number[:8]} - {self.customer_name} ({self.currency} {self.total_in_currency})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=20)
    unit_price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal_usd = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Access token for digital goods / courses
    license_key = models.CharField(max_length=100, blank=True, default='')
    download_url = models.URLField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField(default=timezone.now)
    
    company_name = models.CharField(max_length=200, default='OmniCommerce Global Inc.')
    company_tax_id = models.CharField(max_length=100, default='US-EIN-984321789')
    company_address = models.TextField(default='100 Tech Plaza, Suite 400, San Francisco, CA 94105, USA')
    
    notes = models.TextField(blank=True, default='Thank you for your business. For support visit support@omnicommerce.io')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} (Order {self.order.order_number[:8]})"
