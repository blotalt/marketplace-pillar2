from django.db import models
from django.utils.text import slugify

class ProductType(models.TextChoices):
    PHYSICAL = 'PHYSICAL', 'Physical Hardware'
    DIGITAL = 'DIGITAL', 'Digital Download'
    SAAS = 'SAAS', 'SaaS Subscription Tier'
    COURSE = 'COURSE', 'Educational Course'

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, default='')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    product_type = models.CharField(
        max_length=20,
        choices=ProductType.choices,
        default=ProductType.PHYSICAL
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    short_description = models.CharField(max_length=300, blank=True, default='')
    description = models.TextField(blank=True, default='')
    
    # Pricing (USD base)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_at_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Media & Visuals
    image_url = models.URLField(max_length=500, blank=True, default='')
    badge_label = models.CharField(max_length=50, blank=True, default='')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Social Proof / Ratings
    rating_average = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    rating_count = models.PositiveIntegerField(default=0)
    
    # --- PHYSICAL GOODS FIELDS ---
    sku = models.CharField(max_length=60, blank=True, default='')
    stock_quantity = models.PositiveIntegerField(default=100)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, default=0.50)
    dimensions = models.CharField(max_length=100, blank=True, default='')  # e.g., "20x15x5 cm"
    requires_shipping = models.BooleanField(default=True)
    
    # --- DIGITAL DOWNLOAD FIELDS ---
    file_format = models.CharField(max_length=50, blank=True, default='') # PDF, ZIP, PRESET, VST
    file_size_mb = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    download_link = models.URLField(max_length=500, blank=True, default='')
    preview_sample_url = models.URLField(max_length=500, blank=True, default='')
    license_type = models.CharField(max_length=100, blank=True, default='Commercial Single-User')

    # --- SAAS SUBSCRIPTION FIELDS ---
    billing_interval = models.CharField(max_length=20, blank=True, default='monthly') # monthly / yearly
    trial_period_days = models.PositiveIntegerField(default=14)
    tier_level = models.CharField(max_length=50, blank=True, default='Pro') # Starter, Pro, Enterprise
    features_list = models.JSONField(default=list, blank=True) # list of feature strings

    # --- COURSE FIELDS ---
    duration_hours = models.DecimalField(max_digits=5, decimal_places=1, default=10.0)
    lesson_count = models.PositiveIntegerField(default=12)
    skill_level = models.CharField(max_length=50, blank=True, default='Intermediate') # Beginner, Intermediate, Advanced
    instructor_name = models.CharField(max_length=150, blank=True, default='')
    instructor_title = models.CharField(max_length=150, blank=True, default='')
    syllabus = models.JSONField(default=list, blank=True) # list of modules with lessons

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.product_type != ProductType.PHYSICAL:
            self.requires_shipping = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_product_type_display()})"
