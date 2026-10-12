from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'product', 'product_name', 'author_name', 'author_email',
            'rating', 'title', 'comment', 'is_verified_buyer',
            'photo_url', 'helpful_votes', 'created_at'
        ]
