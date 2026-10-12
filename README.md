# Pillar 2: E-Commerce & Digital Marketplace

A modern, production-ready full-stack marketplace architecture built with **Django REST Framework** on the backend and **Vue 3 (Vite + Pinia + Tailwind CSS)** on the frontend.

## 🚀 Key Features

### 1. Multi-Type Product Catalog
Supports 4 distinct commerce paradigms in a unified catalog:
- 📦 **Physical Hardware**: SKU, stock counts, shipping weight, physical dimensions, low-stock warnings.
- 💾 **Digital Downloads**: Audio presets, UI kits, eBooks, source code with instant download token access.
- ⚡ **SaaS Subscription Tiers**: Monthly/Annual toggle, feature entitlement lists, trial periods, tier levels (Starter, Pro, Enterprise).
- 🎓 **Video & Interactive Courses**: Curriculum syllabi, lesson counters, instructor credentials, difficulty badges.
- **Faceted Filters & Search**: Real-time filtering by category, product type, price range, and star rating.

### 2. Universal Slide-Out Cart & Instant Checkout
- **Slide-out Cart Drawer**: Smooth slide-in from the right, persistent across page navigation.
- **Multi-Currency Engine**: Live conversions across **USD ($)**, **EUR (€)**, **GBP (£)**, **JPY (¥)**, **BTC (₿)**, **ETH (Ξ)**, and **USDT (₮)**.
- **Dynamic Tiered Discount & Free Shipping Progress Bar**:
  - Live progress meter: *"Add $X more to unlock FREE Express Shipping!"* and tiered discount thresholds.
- **Dynamic Coupon / Promo Verification**: Supports fixed amount or percentage deductions with minimum cart value requirements (e.g., `SAVE20`, `DIGITAL50`, `FREESHIP`).
- **Real-Time Tax & Shipping Estimator**: Calculates regional sales tax and distance/tier-based shipping costs dynamically.
- **Instant Checkout Drawer / Modal**: Streamlined payment simulation with mock gateway responses and instant invoice generation.

### 3. Interactive Invoice Generator
- Clean, printable & exportable PDF-ready receipts.
- Live customizer: Edit company details, client information, custom line items, tax rates, payment status, and notes.
- Printable layout with standard business invoice styling and QR verification badge.

### 4. Affiliate & Referral Dashboard
- Custom referral link & code generator with one-click copy.
- Real-time commission analytics: Total Clicks, Referred Orders, Conversion Rate %, Gross Earnings, and Pending Balance.
- Payout transaction ledger with status indicators (`Approved`, `Pending`, `Paid`).

### 5. Customer Review & Social Proof Engine
- 5-Star rating system with interactive summary charts (% distribution of 5, 4, 3, 2, 1 stars).
- **Verified Buyer Badges** on verified purchaser reviews.
- **Photo Upload Testimonials**: Image preview, photo gallery lightbox, and helpful vote counters.
- Filter reviews by rating or toggle "With Photos Only".

---

## 🛠️ Project Structure

```
marketplace_pillar2/
├── backend/                  # Django REST Framework Backend
│   ├── core/                 # Django settings and root URLs
│   ├── products/             # Product models, filters & serializers
│   ├── orders/               # Cart, Checkout, Coupon, Tax & Invoicing
│   ├── affiliates/           # Referral links, commission tracking
│   ├── reviews/              # Star ratings, verified badges, photo reviews
│   ├── seed_data.py          # Database population script
│   ├── manage.py
│   └── requirements.txt
├── frontend/                 # Vue 3 Frontend (Vite + Pinia + Tailwind)
│   ├── src/
│   │   ├── api/              # Axios / Fetch client
│   │   ├── components/       # UI Components (Cart, Checkout, Invoice, etc.)
│   │   ├── stores/           # Pinia stores (Cart, Product, Affiliate, Review)
│   │   ├── data/             # Rich offline demo data
│   │   ├── App.vue           # Main application view with tab navigation
│   │   └── main.js
│   ├── index.html
│   ├── tailwind.config.js
│   └── package.json
└── README.md
```

---

## 💻 Quick Start Guide

### Backend Setup (Django)
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python seed_data.py          # Populates catalog with physical, digital, SaaS, and courses
python manage.py runserver   # Starts API at http://127.0.0.1:8000
```

### Frontend Setup (Vue 3)
```bash
cd frontend
npm install
npm run dev                  # Launches dev server at http://localhost:5173
```
*Note: The frontend operates in dual-mode: it seamlessly interacts with the Django backend at `http://127.0.0.1:8000/api/`, and includes built-in offline mock fallback data so you can test and demonstrate all UI interactions immediately!*
