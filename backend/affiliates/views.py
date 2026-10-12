from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Affiliate, AffiliateReferral, PayoutRecord
from .serializers import AffiliateSerializer

class AffiliateDashboardView(APIView):
    def get(self, request, code=None):
        code = code or request.query_params.get('code', 'CREATOR25')
        affiliate = Affiliate.objects.filter(code=code).first()

        if not affiliate:
            # Create a demo affiliate if none exists yet
            affiliate = Affiliate.objects.create(
                user_name="Alex River (Creator)",
                email="alex@creatorhub.io",
                code=code,
                commission_rate=15.00,
                total_clicks=1420,
                total_earnings_usd=2845.50,
                balance_payable_usd=420.00
            )

        serializer = AffiliateSerializer(affiliate)
        return Response(serializer.data)

class TrackClickView(APIView):
    def post(self, request):
        code = request.data.get('code', '').strip()
        if code:
            affiliate = Affiliate.objects.filter(code=code).first()
            if affiliate:
                affiliate.total_clicks += 1
                affiliate.save()
                return Response({'status': 'click tracked', 'total_clicks': affiliate.total_clicks})
        return Response({'status': 'ignored'}, status=status.HTTP_200_OK)

class RequestPayoutView(APIView):
    def post(self, request):
        code = request.data.get('code', '')
        affiliate = Affiliate.objects.filter(code=code).first()
        if not affiliate:
            return Response({'error': 'Affiliate not found'}, status=status.HTTP_404_NOT_FOUND)
        
        balance = float(affiliate.balance_payable_usd)
        if balance < 50.0:
            return Response({'error': 'Minimum payout balance is $50.00'}, status=status.HTTP_400_BAD_REQUEST)

        PayoutRecord.objects.create(
            affiliate=affiliate,
            amount_usd=affiliate.balance_payable_usd,
            payout_method=request.data.get('method', 'PayPal')
        )
        affiliate.balance_payable_usd = 0.00
        affiliate.save()

        return Response({'message': f'Payout of ${balance:.2f} initiated successfully!'})
