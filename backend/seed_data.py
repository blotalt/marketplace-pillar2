import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product, Category, ProductType
from orders.models import Coupon
from affiliates.models import Affiliate, AffiliateReferral, PayoutRecord
from reviews.models import Review

def run_seed():
    print("Clearing and seeding database with rich marketplace data...")

    # 1. Categories
    cat_hw, _ = Category.objects.get_or_create(
        slug='hardware-gear',
        defaults={'name': 'Hardware & Gear', 'description': 'Ergonomic mechanical hardware and studio peripherals.'}
    )
    cat_digital, _ = Category.objects.get_or_create(
        slug='digital-assets',
        defaults={'name': 'Digital Downloads', 'description': 'Production-ready presets, source kits, and audio packs.'}
    )
    cat_saas, _ = Category.objects.get_or_create(
        slug='saas-subscriptions',
        defaults={'name': 'SaaS Cloud Tools', 'description': 'Developer infrastructure and AI-driven automation workflows.'}
    )
    cat_courses, _ = Category.objects.get_or_create(
        slug='academy-courses',
        defaults={'name': 'Academy Courses', 'description': 'In-depth engineering and system architecture masterclasses.'}
    )

    # 2. Products
    products_data = [
        # PHYSICAL
        {
            'name': 'Apex MechPro Wireless Split Keyboard',
            'product_type': ProductType.PHYSICAL,
            'category': cat_hw,
            'short_description': 'Ultra-ergonomic split mechanical keyboard with hot-swappable switches and CNC aluminum chassis.',
            'description': 'Engineered for developers and creators spending 10+ hours a day typing. Features Bluetooth 5.3 low-latency wireless, custom gateron linear switches, per-key RGB backlighting, and magnetic wrist rests.',
            'price': Decimal('189.00'),
            'compare_at_price': Decimal('229.00'),
            'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=80',
            'badge_label': 'Best Seller',
            'is_featured': True,
            'rating_average': Decimal('4.92'),
            'rating_count': 128,
            'sku': 'HW-KB-APEX01',
            'stock_quantity': 42,
            'weight_kg': Decimal('1.35'),
            'dimensions': '34 x 16 x 3.8 cm',
            'requires_shipping': True,
        },
        {
            'name': 'StudioMaster USB-C Audio Interface 4K',
            'product_type': ProductType.PHYSICAL,
            'category': cat_hw,
            'short_description': '24-bit/192kHz low-noise studio preamp with balanced TRS outputs and zero-latency hardware monitoring.',
            'description': 'Professional desktop audio interface crafted with high-headroom instrument inputs, pristine phantom-powered preamps, and dedicated hardware knobs for headphone mix tracking.',
            'price': Decimal('249.00'),
            'compare_at_price': Decimal('289.00'),
            'image_url': 'https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?auto=format&fit=crop&w=800&q=80',
            'badge_label': 'Staff Pick',
            'is_featured': True,
            'rating_average': Decimal('4.85'),
            'rating_count': 84,
            'sku': 'HW-AUD-SM4K',
            'stock_quantity': 19,
            'weight_kg': Decimal('0.92'),
            'dimensions': '21 x 14 x 5.2 cm',
            'requires_shipping': True,
        },
        {
            'name': 'Aerospace Grade Titanium Laptop Stand',
            'product_type': ProductType.PHYSICAL,
            'category': cat_hw,
            'short_description': 'Laser-cut titanium alloy folding stand with multi-angle height adjustment and passive airflow channel.',
            'description': 'Precision CNC-machined stand capable of supporting up to 17-inch workstations without flexing. Folds flat down to 4mm for effortless travel.',
            'price': Decimal('75.00'),
            'compare_at_price': Decimal('95.00'),
            'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=800&q=80',
            'badge_label': 'Top Rated',
            'is_featured': False,
            'rating_average': Decimal('4.78'),
            'rating_count': 61,
            'sku': 'HW-STD-TITN',
            'stock_quantity': 88,
            'weight_kg': Decimal('0.48'),
            'dimensions': '26 x 22 x 0.4 cm',
            'requires_shipping': True,
        },

        # DIGITAL DOWNLOADS
        {
            'name': 'Cinematic 8K Color Grading LUTs & Grain Pack',
            'product_type': ProductType.DIGITAL,
            'category': cat_digital,
            'short_description': '65+ Hollywood film emulation LUTs (.CUBE) calibrated for Arri, RED, Sony S-Log3, and Apple Log.',
            'description': 'Elevate your commercial video productions in seconds. Includes 16mm/35mm authentic film grain overlays, halation presets, and quick installation guides for DaVinci Resolve, Premiere Pro, and Final Cut.',
            'price': Decimal('39.00'),
            'compare_at_price': Decimal('79.00'),
            'image_url': 'https://images.unsplash.com/photo-1536240478700-b869070f9279?auto=format&fit=crop&w=800&q=80',
            'badge_label': 'Instant ZIP',
            'is_featured': True,
            'rating_average': Decimal('4.96'),
            'rating_count': 312,
            'file_format': 'ZIP Archive (.CUBE + ProRes)',
            'file_size_mb': Decimal('620.00'),
            'download_link': 'https://omnicommerce.io/vault/digital/cinematic-luts-v2.zip',
            'preview_sample_url': 'https://omnicommerce.io/previews/luts-sample.mp4',
            'license_type': 'Commercial Lifetime License',
            'requires_shipping': False,
        },
        {
            'name': 'Modern SaaS Design System (Figma & Tailwind Kit)',
            'product_type': ProductType.DIGITAL,
            'category': cat_digital,
            'short_description': '350+ accessible components, interactive charts, auth flows, and responsive dark-mode layouts.',
            'description': 'Built for engineering teams and indie founders. Includes fully tokenized typography, auto-layout 5.0 components in Figma, and matched ready-to-paste Tailwind CSS & Vue templates.',
            'price': Decimal('59.00'),
            'compare_at_price': Decimal('119.00'),
            'image_url': 'https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?auto=format&fit=crop&w=800&q=80',
            'badge_label': 'Hot Download',
            'is_featured': True,
            'rating_average': Decimal('4.91'),
            'rating_count': 195,
            'file_format': 'Figma File + ZIP Code Bundle',
            'file_size_mb': Decimal('180.50'),
            'download_link': 'https://omnicommerce.io/vault/digital/saas-design-system.zip',
            'license_type': 'Unlimited Client Projects',
            'requires_shipping': False,
        },

        # SAAS TIERS
        {
            'name': 'CloudPulse Distributed Observability - Pro Tier',
            'product_type': ProductType.SAAS,
            'category': cat_saas,
            'short_description': 'Continuous APM metrics, distributed OpenTelemetry tracing, and automated anomaly alert rules.',
            'description': 'Monitor your microservices with sub-second latency analytics. Integrates with Docker, Kubernetes, AWS, and GCP with zero agent friction.',
            'price': Decimal('89.00'),
            'compare_at_price': Decimal('129.00'),
            'image_url': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80',
            'badge_label': '14-Day Free Trial',
            'is_featured': True,
            'rating_average': Decimal('4.88'),
            'rating_count': 77,
            'billing_interval': 'monthly',
            'trial_period_days': 14,
            'tier_level': 'Pro Tier',
            'features_list': [
                'Up to 25,000,000 trace events/month',
                'Distributed OpenTelemetry & Prometheus ingest',
                'Zero-overhead eBPF kernel profiling',
                'Custom alert webhooks (Slack, Discord, PagerDuty)',
                '90-day retention with instant cold-storage search',
                'Dedicated engineer support via shared Slack channel'
            ],
            'requires_shipping': False,
        },
        {
            'name': 'NeuralScribe AI Multilingual Localization Suite',
            'product_type': ProductType.SAAS,
            'category': cat_saas,
            'short_description': 'Automated i18n copy generation, contextual glossaries, and pull request translation automation.',
            'description': 'Keep your apps translated into 64 languages continuously. Seamless GitHub sync triggers PRs whenever your primary translation files change.',
            'price': Decimal('39.00'),
            'compare_at_price': Decimal('59.00'),
            'image_url': 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80',
            'badge_label': 'SaaS Monthly',
            'is_featured': False,
            'rating_average': Decimal('4.74'),
            'rating_count': 53,
            'billing_interval': 'monthly',
            'trial_period_days': 7,
            'tier_level': 'Starter Pro',
            'features_list': [
                '1,000,000 translated tokens/month',
                'Automated GitHub PR localization workflows',
                'Brand tone & terminology glossary lock',
                'Rest API with 99.99% uptime SLA',
                'JSON, YAML, Gettext PO, and Markdown export'
            ],
            'requires_shipping': False,
        },

        # COURSES
        {
            'name': 'High-Scale Distributed Systems Architecture',
            'product_type': ProductType.COURSE,
            'category': cat_courses,
            'short_description': 'Master event-driven architecture, Raft consensus, Kafka partitions, and zero-downtime database sharding.',
            'description': 'A comprehensive masterclass for senior software engineers wanting to step up to Principal Architect. Includes real-world production postmortems, live coding demonstrations in Go and Python, and architectural design blueprints.',
            'price': Decimal('149.00'),
            'compare_at_price': Decimal('249.00'),
            'image_url': 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=800&q=80',
            'badge_label': 'Masterclass',
            'is_featured': True,
            'rating_average': Decimal('4.97'),
            'rating_count': 240,
            'duration_hours': Decimal('26.5'),
            'lesson_count': 54,
            'skill_level': 'Advanced',
            'instructor_name': 'Dr. Elena Rostova',
            'instructor_title': 'Principal Infrastructure Fellow (Ex-Stripe, Ex-AWS)',
            'syllabus': [
                {'module': 'Module 1: Consistency Guarantees & PACELC Theorem', 'lessons': 10, 'duration': '4.5 hrs'},
                {'module': 'Module 2: Event-Driven Log Streaming with Apache Kafka', 'lessons': 12, 'duration': '6.0 hrs'},
                {'module': 'Module 3: Database Sharding, CDC, & Two-Phase Commit', 'lessons': 14, 'duration': '7.2 hrs'},
                {'module': 'Module 4: Resilient Edge Caching & Multi-Region Active-Active', 'lessons': 18, 'duration': '8.8 hrs'}
            ],
            'requires_shipping': False,
        },
        {
            'name': 'The Full-Stack Vue 3 & Django Enterprise Blueprint',
            'product_type': ProductType.COURSE,
            'category': cat_courses,
            'short_description': 'Build multi-tenant SaaS, universal cart checkout, Pinia architecture, and JWT secure auth from scratch.',
            'description': 'Hands-on project-based engineering guide covering DRF best practices, Vue 3 Composition API, custom directives, real-time WebSocket state, and containerized deployment.',
            'price': Decimal('119.00'),
            'compare_at_price': Decimal('189.00'),
            'image_url': 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80',
            'badge_label': 'Certified',
            'is_featured': False,
            'rating_average': Decimal('4.94'),
            'rating_count': 182,
            'duration_hours': Decimal('21.0'),
            'lesson_count': 42,
            'skill_level': 'Intermediate to Advanced',
            'instructor_name': 'Marcus Vance',
            'instructor_title': 'Full-Stack Architecture Lead & Open-Source Contributor',
            'syllabus': [
                {'module': 'Module 1: Production Django REST API & Model Schema', 'lessons': 10, 'duration': '5.0 hrs'},
                {'module': 'Module 2: Vue 3 Composition API, Router & Pinia Stores', 'lessons': 12, 'duration': '5.8 hrs'},
                {'module': 'Module 3: Universal Cart, Multi-Currency & Invoicing Engine', 'lessons': 11, 'duration': '5.2 hrs'},
                {'module': 'Module 4: Automated Testing, CI/CD & Cloud Deployment', 'lessons': 9, 'duration': '5.0 hrs'}
            ],
            'requires_shipping': False,
        }
    ]

    for p_data in products_data:
        p, created = Product.objects.get_or_create(name=p_data['name'], defaults=p_data)
        if created:
            print(f"Created Product: {p.name}")

    # 3. Coupons
    coupons = [
        {'code': 'SAVE20', 'discount_type': 'PERCENT', 'value': Decimal('20.00'), 'min_purchase': Decimal('40.00')},
        {'code': 'DIGITAL50', 'discount_type': 'PERCENT', 'value': Decimal('50.00'), 'min_purchase': Decimal('30.00')},
        {'code': 'FREESHIP', 'discount_type': 'FIXED', 'value': Decimal('15.00'), 'min_purchase': Decimal('0.00')},
        {'code': 'WELCOME10', 'discount_type': 'FIXED', 'value': Decimal('10.00'), 'min_purchase': Decimal('50.00')},
    ]
    for c_data in coupons:
        c, created = Coupon.objects.get_or_create(code=c_data['code'], defaults=c_data)
        if created:
            print(f"Created Coupon: {c.code}")

    # 4. Affiliates
    aff, created = Affiliate.objects.get_or_create(
        code='CREATOR25',
        defaults={
            'user_name': 'Sarah Connor (Tech Creator)',
            'email': 'sarah@techtitan.io',
            'commission_rate': Decimal('15.00'),
            'total_clicks': 1840,
            'total_earnings_usd': Decimal('3420.00'),
            'balance_payable_usd': Decimal('540.00')
        }
    )
    if created:
        print(f"Created Affiliate: {aff.code}")
        # Add sample referrals
        AffiliateReferral.objects.create(
            affiliate=aff,
            order_total_usd=Decimal('189.00'),
            commission_amount_usd=Decimal('28.35'),
            status='approved'
        )
        AffiliateReferral.objects.create(
            affiliate=aff,
            order_total_usd=Decimal('149.00'),
            commission_amount_usd=Decimal('22.35'),
            status='paid'
        )
        PayoutRecord.objects.create(
            affiliate=aff,
            amount_usd=Decimal('450.00'),
            payout_method='PayPal Transfer',
            status='Completed'
        )

    # 5. Reviews
    first_product = Product.objects.first()
    if first_product:
        Review.objects.get_or_create(
            product=first_product,
            author_email='jason.dev@gmail.com',
            defaults={
                'author_name': 'Jason Miller',
                'rating': 5,
                'title': 'Best keyboard purchase I have ever made!',
                'comment': 'The split ergonomics eliminated my wrist fatigue completely within 3 days. The CNC aluminum weight feels exceptionally premium on the desk.',
                'is_verified_buyer': True,
                'photo_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=400&q=80',
                'helpful_votes': 34
            }
        )
        Review.objects.get_or_create(
            product=first_product,
            author_email='sophia.k@studio.com',
            defaults={
                'author_name': 'Sophia Krause',
                'rating': 5,
                'title': 'Stunning build quality and battery life',
                'comment': 'Connects seamlessly to both my Mac Studio and Linux rig via Bluetooth. Zero latency and hot-swappable sockets make customization a breeze.',
                'is_verified_buyer': True,
                'photo_url': 'https://images.unsplash.com/photo-1595225476474-87563907a212?auto=format&fit=crop&w=400&q=80',
                'helpful_votes': 19
            }
        )

    print("Database seeding completed successfully!")

if __name__ == '__main__':
    run_seed()
