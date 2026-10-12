<script setup>
import { ref } from 'vue';
import Navbar from './components/Navbar.vue';
import ProductCatalog from './components/ProductCatalog.vue';
import ProductDetailModal from './components/ProductDetailModal.vue';
import SlideOutCart from './components/SlideOutCart.vue';
import CheckoutModal from './components/CheckoutModal.vue';
import InvoiceGenerator from './components/InvoiceGenerator.vue';
import AffiliateDashboard from './components/AffiliateDashboard.vue';
import ReviewEngine from './components/ReviewEngine.vue';

const activeTab = ref('catalog');
const currentOrderForInvoice = ref(null);

function handleOrderSuccess(order) {
  currentOrderForInvoice.value = order;
}

function handleViewInvoice(order) {
  currentOrderForInvoice.value = order;
  activeTab.value = 'invoice';
}
</script>

<template>
  <div class="min-h-screen bg-slate-900 text-slate-100 flex flex-col justify-between selection:bg-indigo-500 selection:text-white">
    
    <!-- Top Navigation Bar -->
    <Navbar
      :activeTab="activeTab"
      @update:activeTab="activeTab = $event"
    />

    <!-- Main Content Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <!-- Tab 1: Product Catalog -->
      <ProductCatalog v-if="activeTab === 'catalog'" />

      <!-- Tab 2: Interactive Invoice Generator -->
      <InvoiceGenerator
        v-else-if="activeTab === 'invoice'"
        :initialOrder="currentOrderForInvoice"
      />

      <!-- Tab 3: Affiliate & Referral Dashboard -->
      <AffiliateDashboard v-else-if="activeTab === 'affiliate'" />

      <!-- Tab 4: Customer Review Engine -->
      <ReviewEngine v-else-if="activeTab === 'reviews'" />
    </main>

    <!-- Slide-Out Universal Cart Drawer -->
    <SlideOutCart />

    <!-- Instant Checkout Modal -->
    <CheckoutModal
      @order-success="handleOrderSuccess"
      @view-invoice="handleViewInvoice"
    />

    <!-- Deep-Dive Product Detail Modal -->
    <ProductDetailModal />

    <!-- Application Footer -->
    <footer class="bg-slate-950 border-t border-slate-800/80 py-10 mt-16 text-xs text-slate-400">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-6">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-white text-xs">
            Ω
          </div>
          <div>
            <p class="font-bold text-slate-200">OmniCommerce Platform — Pillar 2 Architecture</p>
            <p class="text-[11px] text-slate-500">Django REST Framework Backend + Vue 3 / Pinia / Tailwind Frontend</p>
          </div>
        </div>

        <div class="flex flex-wrap items-center gap-4 text-xs font-medium">
          <span class="text-slate-500">Features:</span>
          <span class="text-slate-300">Multi-Type Catalog</span>
          <span>·</span>
          <span class="text-slate-300">Slide-Out Cart</span>
          <span>·</span>
          <span class="text-slate-300">Multi-Currency (7)</span>
          <span>·</span>
          <span class="text-slate-300">Dynamic Coupons</span>
          <span>·</span>
          <span class="text-slate-300">PDF Invoices</span>
          <span>·</span>
          <span class="text-slate-300">Affiliate Portal</span>
        </div>

        <div class="text-[11px] text-slate-500">
          © 2026 OmniCommerce Inc. All rights reserved.
        </div>
      </div>
    </footer>

  </div>
</template>
