import uuid
from decimal import Decimal
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from .models import Order, OrderItem, Coupon, Invoice
from .serializers import OrderSerializer, InvoiceSerializer
from products.models import Product

# Exchange rates relative to 1.0 USD
EXCHANGE_RATES = {
    'USD': Decimal('1.0000'),
    'EUR': Decimal('0.9200'),
    'GBP': Decimal('0.7900'),
    'JPY': Decimal('155.2000'),
    'BTC': Decimal('0.000015'),
    'ETH': Decimal('0.000290'),
    'USDT': Decimal('1.0000'),
}

COUNTRY_TAX_RATES = {
    'United States': Decimal('0.0825'),
    'Germany': Decimal('0.1900'),
    'United Kingdom': Decimal('0.2000'),
    'France': Decimal('0.2000'),
    'Japan': Decimal('0.1000'),
    'Canada': Decimal('0.1300'),
    'Australia': Decimal('0.1000'),
    'Singapore': Decimal('0.0900'),
}

FREE_SHIPPING_THRESHOLD_USD = Decimal('100.00')

class VerifyCouponView(APIView):
    def post(self, request):
        code = request.data.get('code', '').strip().upper()
        subtotal = float(request.data.get('subtotal', 0.0))

        if not code:
            return Response({'valid': False, 'message': 'Coupon code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            coupon = Coupon.objects.get(code=code)
            is_valid, message = coupon.is_valid_for(subtotal)
            if not is_valid:
                return Response({'valid': False, 'message': message}, status=status.HTTP_200_OK)

            discount_usd = coupon.calculate_discount(subtotal)
            return Response({
                'valid': True,
                'code': coupon.code,
                'discount_type': coupon.discount_type,
                'value': float(coupon.value),
                'discount_usd': discount_usd,
                'message': f"Coupon '{coupon.code}' applied successfully!"
            }, status=status.HTTP_200_OK)

        except Coupon.DoesNotExist:
            # Fallback for dynamic demo coupons if database hasn't been seeded yet
            if code == 'SAVE20':
                discount = round(subtotal * 0.20, 2)
                return Response({'valid': True, 'code': 'SAVE20', 'discount_usd': discount, 'message': '20% Off Applied!'}, status=200)
            elif code == 'DIGITAL50':
                discount = round(subtotal * 0.50, 2)
                return Response({'valid': True, 'code': 'DIGITAL50', 'discount_usd': discount, 'message': '50% Off Digital Pass Applied!'}, status=200)
            elif code == 'FREESHIP':
                return Response({'valid': True, 'code': 'FREESHIP', 'discount_usd': 0.00, 'free_shipping': True, 'message': 'Free Shipping Unlocked!'}, status=200)

            return Response({'valid': False, 'message': 'Invalid promo or coupon code.'}, status=status.HTTP_200_OK)


class CalculateCheckoutView(APIView):
    def post(self, request):
        items = request.data.get('items', [])
        currency = request.data.get('currency', 'USD').upper()
        country = request.data.get('country', 'United States')
        shipping_tier = request.data.get('shipping_tier', 'standard')
        coupon_code = request.data.get('coupon_code', '').strip().upper()

        exchange_rate = EXCHANGE_RATES.get(currency, Decimal('1.0000'))
        
        # Calculate subtotal and inspect product requirements
        subtotal_usd = Decimal('0.00')
        has_physical_items = False

        for item in items:
            qty = int(item.get('quantity', 1))
            unit_price = Decimal(str(item.get('price', 0.00)))
            subtotal_usd += unit_price * qty
            
            p_type = item.get('product_type', '').upper()
            if p_type == 'PHYSICAL' or item.get('requires_shipping', False):
                has_physical_items = True

        # Tiered shipping calculation & Free Shipping progress bar
        threshold = FREE_SHIPPING_THRESHOLD_USD
        shipping_usd = Decimal('0.00')
        amount_needed_for_free_shipping = Decimal('0.00')
        free_shipping_unlocked = False

        if has_physical_items:
            if subtotal_usd >= threshold or coupon_code == 'FREESHIP':
                free_shipping_unlocked = True
                shipping_usd = Decimal('15.00') if shipping_tier == 'express' else Decimal('0.00')
                amount_needed_for_free_shipping = Decimal('0.00')
            else:
                amount_needed_for_free_shipping = threshold - subtotal_usd
                shipping_usd = Decimal('25.00') if shipping_tier == 'express' else Decimal('12.00')
        
        progress_percentage = min(100, int((float(subtotal_usd) / float(threshold)) * 100))

        # Dynamic Coupon Discount
        discount_usd = Decimal('0.00')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                is_valid, _ = coupon.is_valid_for(float(subtotal_usd))
                if is_valid:
                    discount_usd = Decimal(str(coupon.calculate_discount(float(subtotal_usd))))
            except Coupon.DoesNotExist:
                if coupon_code == 'SAVE20':
                    discount_usd = (subtotal_usd * Decimal('0.20')).quantize(Decimal('0.01'))
                elif coupon_code == 'DIGITAL50':
                    discount_usd = (subtotal_usd * Decimal('0.50')).quantize(Decimal('0.01'))

        # Tax estimation
        tax_rate = COUNTRY_TAX_RATES.get(country, Decimal('0.0500'))
        taxable_amount = max(Decimal('0.00'), subtotal_usd - discount_usd)
        tax_usd = (taxable_amount * tax_rate).quantize(Decimal('0.01'))

        # Final totals
        total_usd = max(Decimal('0.00'), taxable_amount + shipping_usd + tax_usd)
        total_in_currency = (total_usd * exchange_rate).quantize(Decimal('0.0001' if 'BTC' in currency or 'ETH' in currency else '0.01'))

        return Response({
            'currency': currency,
            'exchange_rate': float(exchange_rate),
            'subtotal_usd': float(subtotal_usd),
            'discount_usd': float(discount_usd),
            'shipping_usd': float(shipping_usd),
            'tax_usd': float(tax_usd),
            'total_usd': float(total_usd),
            'total_in_currency': float(total_in_currency),
            'has_physical_items': has_physical_items,
            'free_shipping_threshold': float(threshold),
            'free_shipping_unlocked': free_shipping_unlocked,
            'amount_needed_for_free_shipping': float(amount_needed_for_free_shipping),
            'progress_percentage': progress_percentage,
            'tax_rate_percent': float(tax_rate * 100),
        })


class CreateOrderView(APIView):
    def post(self, request):
        data = request.data
        items_data = data.get('items', [])
        if not items_data:
            return Response({'error': 'Cannot create order with an empty cart.'}, status=status.HTTP_400_BAD_REQUEST)

        currency = data.get('currency', 'USD').upper()
        exchange_rate = EXCHANGE_RATES.get(currency, Decimal('1.0000'))
        
        customer_name = data.get('customer_name', 'Valued Customer')
        customer_email = data.get('customer_email', 'customer@example.com')
        customer_country = data.get('customer_country', 'United States')
        shipping_address = data.get('shipping_address', '123 Market Street, Suite 1')
        
        subtotal_usd = Decimal(str(data.get('subtotal_usd', '0.00')))
        discount_usd = Decimal(str(data.get('discount_usd', '0.00')))
        shipping_usd = Decimal(str(data.get('shipping_usd', '0.00')))
        tax_usd = Decimal(str(data.get('tax_usd', '0.00')))
        total_usd = Decimal(str(data.get('total_usd', '0.00')))
        total_in_currency = Decimal(str(data.get('total_in_currency', total_usd * exchange_rate)))

        coupon_code = data.get('coupon_code', '')
        referral_code = data.get('referral_code', '')
        payment_method = data.get('payment_method', 'Credit Card')

        order_num = f"ORD-{uuid.uuid4().hex[:10].upper()}"

        order = Order.objects.create(
            order_number=order_num,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_country=customer_country,
            shipping_address=shipping_address,
            currency=currency,
            exchange_rate=exchange_rate,
            subtotal_usd=subtotal_usd,
            discount_usd=discount_usd,
            shipping_usd=shipping_usd,
            tax_usd=tax_usd,
            total_usd=total_usd,
            total_in_currency=total_in_currency,
            coupon_code=coupon_code,
            referral_code=referral_code,
            payment_method=payment_method,
            payment_status='PAID'
        )

        for item in items_data:
            p_id = item.get('id')
            product = None
            if p_id:
                product = Product.objects.filter(id=p_id).first()
                if product and product.product_type == 'PHYSICAL':
                    product.stock_quantity = max(0, product.stock_quantity - int(item.get('quantity', 1)))
                    product.save()

            license_key = f"KEY-{uuid.uuid4().hex[:12].upper()}" if item.get('product_type') in ['DIGITAL', 'SAAS', 'COURSE'] else ''
            download_url = item.get('download_link', 'https://omnicommerce.io/downloads/asset-vault.zip')

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=item.get('name', 'Marketplace Item'),
                product_type=item.get('product_type', 'DIGITAL'),
                unit_price_usd=Decimal(str(item.get('price', 0.00))),
                quantity=int(item.get('quantity', 1)),
                subtotal_usd=Decimal(str(item.get('price', 0.00))) * int(item.get('quantity', 1)),
                license_key=license_key,
                download_url=download_url
            )

        # Increment coupon usage if valid
        if coupon_code:
            Coupon.objects.filter(code=coupon_code).update(usage_count=models.F('usage_count') + 1)

        # Trigger affiliate commission credit if referral_code exists
        if referral_code:
            try:
                from affiliates.models import Affiliate, AffiliateReferral
                affiliate = Affiliate.objects.filter(code=referral_code).first()
                if affiliate:
                    comm_amount = (total_usd * (affiliate.commission_rate / Decimal('100.00'))).quantize(Decimal('0.01'))
                    AffiliateReferral.objects.create(
                        affiliate=affiliate,
                        order=order,
                        order_total_usd=total_usd,
                        commission_amount_usd=comm_amount,
                        status='approved'
                    )
                    affiliate.total_earnings_usd += comm_amount
                    affiliate.balance_payable_usd += comm_amount
                    affiliate.save()
            except Exception:
                pass

        # Create Invoice
        invoice_num = f"INV-{timezone.now().strftime('%Y%m')}-{order_num[4:10]}"
        invoice = Invoice.objects.create(
            invoice_number=invoice_num,
            order=order,
            company_name="OmniCommerce Global Inc.",
            company_tax_id="US-EIN-984321789",
            company_address="100 Tech Plaza, Suite 400, San Francisco, CA 94105, USA",
            notes=f"Thank you for ordering with OmniCommerce! Order ID: {order_num}."
        )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InvoiceDetailView(generics.RetrieveAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    lookup_field = 'invoice_number'
