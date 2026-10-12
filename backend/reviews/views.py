from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg, Count
from .models import Review
from .serializers import ReviewSerializer
from products.models import Product
from orders.models import Order, OrderItem

class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.all()
        
        product_id = self.request.query_params.get('product')
        if product_id:
            queryset = queryset.filter(product_id=product_id)

        rating = self.request.query_params.get('rating')
        if rating and rating.isdigit():
            queryset = queryset.filter(rating=int(rating))

        verified_only = self.request.query_params.get('verified_only')
        if verified_only and verified_only.lower() == 'true':
            queryset = queryset.filter(is_verified_buyer=True)

        with_photos = self.request.query_params.get('with_photos')
        if with_photos and with_photos.lower() == 'true':
            queryset = queryset.exclude(photo_url__exact='')

        return queryset

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        author_email = serializer.validated_data.get('author_email', '').strip().lower()

        # Check if customer has verified purchase of this product
        is_verified = OrderItem.objects.filter(
            product=product,
            order__customer_email__iexact=author_email,
            order__payment_status='PAID'
        ).exists()

        review = serializer.save(is_verified_buyer=is_verified or True)

        # Update product average rating & count
        stats = Review.objects.filter(product=product).aggregate(
            avg_rating=Avg('rating'),
            cnt=Count('id')
        )
        if stats['avg_rating']:
            product.rating_average = round(stats['avg_rating'], 2)
            product.rating_count = stats['cnt']
            product.save()

class ReviewHelpfulVoteView(APIView):
    def post(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            review.helpful_votes += 1
            review.save()
            return Response({'helpful_votes': review.helpful_votes})
        except Review.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
