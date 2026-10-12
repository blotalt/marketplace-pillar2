<script setup>
import { computed } from 'vue';
import { useCartStore } from '../stores/cartStore';
import { CURRENCY_RATES } from '../data/mockData';

const props = defineProps({
  activeTab: {
    type: String,
    default: 'catalog'
  }
});

const emit = defineEmits(['update:activeTab']);

const cartStore = useCartStore();

const currencies = Object.values(CURRENCY_RATES);

function setTab(tab) {
  emit('update:activeTab', tab);
}
</script>

<template>
  <header class="sticky top-0 z-40 bg-slate-900/95 backdrop-blur-md border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-20">
        
        <!-- Logo / Brand -->
        <div class="flex items-center space-x-3 cursor-pointer" @click="setTab('catalog')">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-500 flex items-center justify-center shadow-lg shadow-indigo-500/25">
            <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
          </div>
          <div>
            <div class="flex items-center space-x-2">
              <span class="font-extrabold text-xl tracking-tight text-white">OmniCommerce</span>
              <span class="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">Pillar 2</span>
            </div>
            <p class="text-xs text-slate-400">Physical · Digital · SaaS · Courses</p>
          </div>
        </div>

        <!-- Navigation Tabs -->
        <nav class="hidden md:flex items-center space-x-1 bg-slate-800/60 p-1.5 rounded-2xl border border-slate-700/60">
          <button
            @click="setTab('catalog')"
            :class="[
              'px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200 flex items-center space-x-2',
              activeTab === 'catalog'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/25'
                : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
            ]"
          >
            <span>🛍️ Marketplace</span>
          </button>

          <button
            @click="setTab('invoice')"
            :class="[
              'px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200 flex items-center space-x-2',
              activeTab === 'invoice'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/25'
                : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
            ]"
          >
            <span>🧾 Invoice Generator</span>
          </button>

          <button
            @click="setTab('affiliate')"
            :class="[
              'px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200 flex items-center space-x-2',
              activeTab === 'affiliate'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/25'
                : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
            ]"
          >
            <span>🤝 Affiliates</span>
          </button>

          <button
            @click="setTab('reviews')"
            :class="[
              'px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200 flex items-center space-x-2',
              activeTab === 'reviews'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/25'
                : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
            ]"
          >
            <span>⭐ Reviews</span>
          </button>
        </nav>

        <!-- Right Side: Currency Switcher & Slide-Out Cart Trigger -->
        <div class="flex items-center space-x-4">
          <!-- Currency Switcher -->
          <div class="relative">
            <select
              :value="cartStore.currency"
              @change="cartStore.setCurrency($event.target.value)"
              class="appearance-none bg-slate-800 text-slate-200 text-sm font-medium rounded-xl pl-3 pr-8 py-2 border border-slate-700 hover:border-slate-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer"
            >
              <option v-for="c in currencies" :key="c.code" :value="c.code">
                {{ c.code }} ({{ c.symbol }})
              </option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-slate-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>

          <!-- Slide-out Cart Drawer Button -->
          <button
            @click="cartStore.toggleCart()"
            class="relative flex items-center space-x-2.5 px-4 py-2 rounded-xl bg-gradient-to-r from-indigo-600 to-indigo-500 text-white font-semibold text-sm hover:from-indigo-500 hover:to-indigo-400 transition-all duration-200 shadow-lg shadow-indigo-600/20 active:scale-95"
            aria-label="View Cart"
          >
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <span class="hidden sm:inline">Cart</span>
            <span class="inline-flex items-center justify-center min-w-[20px] h-5 px-1.5 rounded-full text-xs font-bold bg-white text-indigo-700">
              {{ cartStore.itemCount }}
            </span>
          </button>
        </div>

      </div>

      <!-- Mobile navigation pills -->
      <div class="md:hidden flex items-center space-x-2 pb-3 overflow-x-auto">
        <button
          @click="setTab('catalog')"
          :class="['px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap', activeTab === 'catalog' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-300']"
        >🛍️ Marketplace</button>
        <button
          @click="setTab('invoice')"
          :class="['px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap', activeTab === 'invoice' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-300']"
        >🧾 Invoices</button>
        <button
          @click="setTab('affiliate')"
          :class="['px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap', activeTab === 'affiliate' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-300']"
        >🤝 Affiliates</button>
        <button
          @click="setTab('reviews')"
          :class="['px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap', activeTab === 'reviews' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-300']"
        >⭐ Reviews</button>
      </div>

    </div>
  </header>
</template>
