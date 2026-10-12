from django.urls import path
from .views import AffiliateDashboardView, TrackClickView, RequestPayoutView

urlpatterns = [
    path('dashboard/', AffiliateDashboardView.as_view(), name='affiliate-dashboard-default'),
    path('dashboard/<str:code>/', AffiliateDashboardView.as_view(), name='affiliate-dashboard'),
    path('track-click/', TrackClickView.as_view(), name='affiliate-track-click'),
    path('request-payout/', RequestPayoutView.as_view(), name='affiliate-request-payout'),
]
