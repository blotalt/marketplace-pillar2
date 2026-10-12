from django.urls import path
from .views import VerifyCouponView, CalculateCheckoutView, CreateOrderView, InvoiceDetailView

urlpatterns = [
    path('coupon/verify/', VerifyCouponView.as_view(), name='coupon-verify'),
    path('calculate/', CalculateCheckoutView.as_view(), name='checkout-calculate'),
    path('create/', CreateOrderView.as_view(), name='order-create'),
    path('invoices/<str:invoice_number>/', InvoiceDetailView.as_view(), name='invoice-detail'),
]
