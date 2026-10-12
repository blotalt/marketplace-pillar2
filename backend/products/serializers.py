from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    product_type_display = serializers.CharField(source='get_product_type_display', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'product_type', 'product_type_display',
            'category', 'category_name', 'short_description', 'description',
            'price', 'compare_at_price', 'image_url', 'badge_label',
            'is_featured', 'is_active', 'rating_average', 'rating_count',
            
            # Physical
            'sku', 'stock_quantity', 'weight_kg', 'dimensions', 'requires_shipping',
            
            # Digital
            'file_format', 'file_size_mb', 'download_link', 'preview_sample_url', 'license_type',
            
            # SaaS
            'billing_interval', 'trial_period_days', 'tier_level', 'features_list',
            
            # Course
            'duration_hours', 'lesson_count', 'skill_level', 'instructor_name', 'instructor_title', 'syllabus',
            
            'created_at', 'updated_at'
        ]
