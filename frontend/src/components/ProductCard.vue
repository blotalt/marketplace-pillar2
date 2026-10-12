<script setup>
import { useCartStore } from '../stores/cartStore';
import { useProductStore } from '../stores/productStore';

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
});

const cartStore = useCartStore();
const productStore = useProductStore();

function getTypeBadge(type) {
  switch (type) {
    case 'PHYSICAL':
      return { label: 'Physical Hardware', icon: '📦', color: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' };
    case 'DIGITAL':
      return { label: 'Digital Download', icon: '💾', color: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20' };
    case 'SAAS':
      return { label: 'SaaS Subscription', icon: '⚡', color: 'bg-amber-500/10 text-amber-400 border-amber-500/20' };
    case 'COURSE':
      return { label: 'Video Course', icon: '🎓', color: 'bg-purple-500/10 text-purple-400 border-purple-500/20' };
    default:
      return { label: 'Product', icon: '🏷️', color: 'bg-slate-700 text-slate-300' };
  }
}
</script>

<template>
  <div class="group relative bg-slate-800/80 rounded-2xl border border-slate-700/80 hover:border-indigo-500/50 transition-all duration-300 flex flex-col overflow-hidden hover:shadow-xl hover:shadow-indigo-500/10 hover:-translate-y-1">
    
    <!-- Image Header & Badges -->
    <div class="relative h-52 w-full overflow-hidden bg-slate-900">
      <img
        :src="product.image_url"
        :alt="product.name"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 opacity-90 group-hover:opacity-100"
        loading="lazy"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-slate-900 via-transparent to-transparent"></div>

      <!-- Top Badges -->
      <div class="absolute top-3 left-3 flex flex-wrap gap-1.5">
        <span
          :class="['text-xs font-semibold px-2.5 py-1 rounded-lg border backdrop-blur-md flex items-center space-x-1', getTypeBadge(product.product_type).color]"
        >
          <span>{{ getTypeBadge(product.product_type).icon }}</span>
          <span>{{ getTypeBadge(product.product_type).label }}</span>
        </span>
      </div>

      <div v-if="product.badge_label" class="absolute top-3 right-3">
        <span class="text-xs font-bold px-2.5 py-1 rounded-lg bg-indigo-600/90 text-white shadow-md backdrop-blur-md">
          {{ product.badge_label }}
        </span>
      </div>

      <!-- Price overlay in image bottom -->
      <div class="absolute bottom-3 right-3 flex items-baseline space-x-2">
        <span v-if="product.compare_at_price" class="text-xs text-slate-400 line-through">
          {{ cartStore.formatCurrency(product.compare_at_price) }}
        </span>
        <span class="text-lg font-extrabold text-white bg-slate-900/80 px-2.5 py-0.5 rounded-lg border border-slate-700/80">
          {{ cartStore.formatCurrency(product.price) }}
        </span>
      </div>
    </div>

    <!-- Content Body -->
    <div class="p-5 flex-1 flex flex-col justify-between">
      <div>
        <!-- Category & Rating -->
        <div class="flex items-center justify-between text-xs text-slate-400 mb-2">
          <span>{{ product.category }}</span>
          <div class="flex items-center space-x-1 text-amber-400">
            <span>★</span>
            <span class="font-bold text-slate-200">{{ product.rating_average }}</span>
            <span class="text-slate-500">({{ product.rating_count }})</span>
          </div>
        </div>

        <!-- Product Title -->
        <h3
          @click="productStore.openProductModal(product)"
          class="font-bold text-base text-white group-hover:text-indigo-400 transition-colors line-clamp-1 cursor-pointer"
        >
          {{ product.name }}
        </h3>

        <!-- Description -->
        <p class="text-xs text-slate-400 mt-2 line-clamp-2 leading-relaxed">
          {{ product.short_description }}
        </p>

        <!-- Dynamic Spec Chips based on Product Type -->
        <div class="mt-4 pt-3 border-t border-slate-700/60 flex flex-wrap gap-2 text-[11px] text-slate-300">
          <!-- Physical specs -->
          <template v-if="product.product_type === 'PHYSICAL'">
            <span class="bg-slate-700/50 px-2 py-0.5 rounded border border-slate-600/50 flex items-center space-x-1">
              <span>📦</span>
              <span>Stock: {{ product.stock_quantity }} units</span>
            </span>
            <span v-if="product.weight_kg" class="bg-slate-700/50 px-2 py-0.5 rounded border border-slate-600/50">
              ⚖️ {{ product.weight_kg }} kg
            </span>
          </template>

          <!-- Digital specs -->
          <template v-if="product.product_type === 'DIGITAL'">
            <span class="bg-cyan-950/40 text-cyan-300 px-2 py-0.5 rounded border border-cyan-800/40">
              ⚡ Instant Download ({{ product.file_size_mb }} MB)
            </span>
            <span class="bg-slate-700/50 px-2 py-0.5 rounded border border-slate-600/50">
              {{ product.file_format }}
            </span>
          </template>

          <!-- SaaS specs -->
          <template v-if="product.product_type === 'SAAS'">
            <span class="bg-amber-950/40 text-amber-300 px-2 py-0.5 rounded border border-amber-800/40">
              🔁 Billed {{ product.billing_interval }}
            </span>
            <span class="bg-slate-700/50 px-2 py-0.5 rounded border border-slate-600/50">
              {{ product.trial_period_days }}-Day Trial
            </span>
          </template>

          <!-- Course specs -->
          <template v-if="product.product_type === 'COURSE'">
            <span class="bg-purple-950/40 text-purple-300 px-2 py-0.5 rounded border border-purple-800/40">
              ⏱️ {{ product.duration_hours }} hrs
            </span>
            <span class="bg-slate-700/50 px-2 py-0.5 rounded border border-slate-600/50">
              📚 {{ product.lesson_count }} Lessons ({{ product.skill_level }})
            </span>
          </template>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="mt-5 grid grid-cols-2 gap-2 pt-2">
        <button
          @click="productStore.openProductModal(product)"
          class="w-full py-2 px-3 rounded-xl bg-slate-700 hover:bg-slate-600 text-slate-200 text-xs font-semibold transition-all duration-200 text-center"
        >
          View Specs
        </button>
        <button
          @click="cartStore.addItem(product)"
          class="w-full py-2 px-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition-all duration-200 flex items-center justify-center space-x-1 shadow-md shadow-indigo-600/20 active:scale-95"
        >
          <span>Add to Cart</span>
          <span>+</span>
        </button>
      </div>

    </div>
  </div>
</template>
