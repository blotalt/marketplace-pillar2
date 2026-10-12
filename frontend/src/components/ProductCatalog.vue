<script setup>
import { onMounted } from 'vue';
import { useProductStore } from '../stores/productStore';
import ProductCard from './ProductCard.vue';

const productStore = useProductStore();

onMounted(() => {
  productStore.loadProducts();
});

const filterTabs = [
  { key: 'ALL', label: 'All Products', icon: '🌐' },
  { key: 'PHYSICAL', label: 'Physical Hardware', icon: '📦' },
  { key: 'DIGITAL', label: 'Digital Downloads', icon: '💾' },
  { key: 'SAAS', label: 'SaaS Tiers', icon: '⚡' },
  { key: 'COURSE', label: 'Courses & Masterclasses', icon: '🎓' },
];
</script>

<template>
  <div class="space-y-8">
    
    <!-- Hero / Headline -->
    <div class="relative overflow-hidden rounded-3xl bg-gradient-to-r from-indigo-950/80 via-slate-900 to-purple-950/80 border border-indigo-900/40 p-8 sm:p-12 shadow-2xl">
      <div class="absolute -right-10 -bottom-10 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div class="max-w-3xl">
        <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-bold tracking-wide uppercase mb-4 border border-indigo-500/30">
          <span>🚀 Pillar 2: E-Commerce & Digital Marketplace</span>
        </div>
        <h1 class="text-3xl sm:text-5xl font-extrabold text-white tracking-tight leading-tight">
          Sell physical goods, digital assets, SaaS tiers, and courses.
        </h1>
        <p class="mt-4 text-base sm:text-lg text-slate-300 leading-relaxed">
          Universal multi-currency checkout, dynamic promo codes, interactive PDF invoices, affiliate attribution, and verified customer testimonials.
        </p>

        <!-- Quick feature badges -->
        <div class="mt-6 flex flex-wrap gap-2 text-xs font-semibold text-slate-300">
          <span class="bg-slate-800/80 border border-slate-700 px-3 py-1.5 rounded-xl">⚡ Universal Slide-Out Cart</span>
          <span class="bg-slate-800/80 border border-slate-700 px-3 py-1.5 rounded-xl">💱 7 Currencies + Crypto</span>
          <span class="bg-slate-800/80 border border-slate-700 px-3 py-1.5 rounded-xl">🏷️ Dynamic Promo Codes (SAVE20, DIGITAL50)</span>
          <span class="bg-slate-800/80 border border-slate-700 px-3 py-1.5 rounded-xl">🧾 One-Click PDF Invoices</span>
        </div>
      </div>
    </div>

    <!-- Filter & Search Control Bar -->
    <div class="bg-slate-800/60 p-4 sm:p-5 rounded-2xl border border-slate-700/60 backdrop-blur-sm space-y-4">
      
      <!-- Type Filter Pills -->
      <div class="flex items-center space-x-2 overflow-x-auto pb-1 sm:pb-0">
        <button
          v-for="tab in filterTabs"
          :key="tab.key"
          @click="productStore.setSelectedType(tab.key)"
          :class="[
            'px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all duration-200 flex items-center space-x-2 whitespace-nowrap',
            productStore.selectedType === tab.key
              ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/25 ring-2 ring-indigo-400/40'
              : 'bg-slate-900/60 text-slate-300 hover:text-white hover:bg-slate-700/60 border border-slate-700/40'
          ]"
        >
          <span>{{ tab.icon }}</span>
          <span>{{ tab.label }}</span>
          <span
            :class="[
              'text-[10px] px-1.5 py-0.5 rounded-full font-bold ml-1',
              productStore.selectedType === tab.key ? 'bg-white/20 text-white' : 'bg-slate-800 text-slate-400'
            ]"
          >
            {{ productStore.typeCounts[tab.key] || 0 }}
          </span>
        </button>
      </div>

      <!-- Search & Sort Row -->
      <div class="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2 border-t border-slate-700/40">
        <!-- Search bar -->
        <div class="relative w-full sm:w-80">
          <input
            type="text"
            v-model="productStore.searchQuery"
            placeholder="Search products, formats, or skills..."
            class="w-full bg-slate-900 text-slate-100 placeholder-slate-500 text-sm rounded-xl pl-10 pr-4 py-2.5 border border-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <button
            v-if="productStore.searchQuery"
            @click="productStore.searchQuery = ''"
            class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-white"
          >
            ✕
          </button>
        </div>

        <!-- Sort dropdown -->
        <div class="flex items-center space-x-3 w-full sm:w-auto justify-end">
          <span class="text-xs text-slate-400 whitespace-nowrap">Sort by:</span>
          <select
            :value="productStore.sortOrder"
            @change="productStore.setSortOrder($event.target.value)"
            class="bg-slate-900 text-slate-200 text-sm font-medium rounded-xl px-3 py-2 border border-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer"
          >
            <option value="featured">✨ Featured & Recommended</option>
            <option value="price_asc">💵 Price: Low to High</option>
            <option value="price_desc">💎 Price: High to Low</option>
            <option value="rating">⭐ Highest Rated</option>
          </select>
        </div>
      </div>

    </div>

    <!-- Product Grid -->
    <div v-if="productStore.filteredProducts.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <ProductCard
        v-for="product in productStore.filteredProducts"
        :key="product.id"
        :product="product"
      />
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-20 bg-slate-800/40 rounded-3xl border border-slate-800">
      <div class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-slate-800 flex items-center justify-center text-3xl">
        🔍
      </div>
      <h3 class="text-lg font-bold text-white">No products found</h3>
      <p class="text-sm text-slate-400 mt-1 max-w-sm mx-auto">
        Try adjusting your filter category or searching for another keyword.
      </p>
      <button
        @click="productStore.setSelectedType('ALL'); productStore.searchQuery = '';"
        class="mt-4 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-xl"
      >
        Reset Filters
      </button>
    </div>

  </div>
</template>
