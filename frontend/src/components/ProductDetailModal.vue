<script setup>
import { computed } from 'vue';
import { useProductStore } from '../stores/productStore';
import { useCartStore } from '../stores/cartStore';

const productStore = useProductStore();
const cartStore = useCartStore();

const product = computed(() => productStore.selectedProductForModal);

function addToCart() {
  if (product.value) {
    cartStore.addItem(product.value);
    productStore.closeProductModal();
  }
}
</script>

<template>
  <div v-if="product" class="fixed inset-0 z-50 overflow-y-auto flex items-center justify-center p-4 sm:p-6">
    <!-- Backdrop -->
    <div
      class="fixed inset-0 bg-slate-950/80 backdrop-blur-md transition-opacity"
      @click="productStore.closeProductModal()"
    ></div>

    <!-- Modal Dialog -->
    <div class="relative bg-slate-900 border border-slate-700/80 rounded-3xl max-w-3xl w-full shadow-2xl overflow-hidden z-10 max-h-[90vh] flex flex-col">
      
      <!-- Close button -->
      <button
        @click="productStore.closeProductModal()"
        class="absolute top-4 right-4 z-20 w-10 h-10 rounded-full bg-slate-800/80 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center backdrop-blur-md transition-colors"
      >
        ✕
      </button>

      <!-- Scrollable content -->
      <div class="overflow-y-auto p-6 sm:p-8 space-y-6">
        
        <!-- Header row with Image and basic metadata -->
        <div class="flex flex-col sm:flex-row gap-6">
          <div class="sm:w-1/2 rounded-2xl overflow-hidden bg-slate-950 h-64 sm:h-auto border border-slate-800 relative">
            <img :src="product.image_url" :alt="product.name" class="w-full h-full object-cover" />
            <div v-if="product.badge_label" class="absolute top-3 left-3 px-2.5 py-1 rounded-lg bg-indigo-600 text-xs font-bold text-white shadow-md">
              {{ product.badge_label }}
            </div>
          </div>

          <div class="sm:w-1/2 flex flex-col justify-between">
            <div>
              <div class="flex items-center space-x-2 text-xs text-indigo-400 font-bold uppercase tracking-wider">
                <span>{{ product.category }}</span>
                <span>•</span>
                <span>{{ product.product_type }}</span>
              </div>
              <h2 class="text-xl sm:text-2xl font-extrabold text-white mt-1">{{ product.name }}</h2>

              <div class="flex items-center space-x-2 mt-2">
                <span class="text-amber-400 text-sm">★ {{ product.rating_average }}</span>
                <span class="text-slate-500 text-xs">({{ product.rating_count }} customer reviews)</span>
              </div>

              <p class="text-xs sm:text-sm text-slate-300 mt-3 leading-relaxed">
                {{ product.description || product.short_description }}
              </p>
            </div>

            <!-- Price and Cart Button -->
            <div class="mt-6 pt-4 border-t border-slate-800 flex items-center justify-between">
              <div>
                <span class="text-xs text-slate-400 block">Unit Price ({{ cartStore.currency }}):</span>
                <span class="text-2xl font-extrabold text-white">
                  {{ cartStore.formatCurrency(product.price) }}
                </span>
              </div>
              <button
                @click="addToCart"
                class="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-sm rounded-xl shadow-lg shadow-indigo-600/30 transition-transform active:scale-95"
              >
                Add to Cart 🛒
              </button>
            </div>
          </div>
        </div>

        <!-- Detailed Multi-Type Specifications Section -->
        <div class="bg-slate-800/60 rounded-2xl p-5 border border-slate-700/60">
          <h4 class="text-sm font-bold text-white uppercase tracking-wider mb-3">Specification & Licensing</h4>

          <!-- PHYSICAL GOODS SPECIFICATIONS -->
          <div v-if="product.product_type === 'PHYSICAL'" class="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
            <div class="bg-slate-900/60 p-3 rounded-xl border border-slate-800">
              <span class="text-slate-400 block mb-1">SKU Code</span>
              <span class="font-mono font-bold text-slate-200">{{ product.sku || 'HW-GEN-01' }}</span>
            </div>
            <div class="bg-slate-900/60 p-3 rounded-xl border border-slate-800">
              <span class="text-slate-400 block mb-1">In Warehouse</span>
              <span class="font-bold text-emerald-400">{{ product.stock_quantity }} units ready</span>
            </div>
            <div class="bg-slate-900/60 p-3 rounded-xl border border-slate-800">
              <span class="text-slate-400 block mb-1">Shipping Weight</span>
              <span class="font-bold text-slate-200">{{ product.weight_kg }} kg</span>
            </div>
            <div class="bg-slate-900/60 p-3 rounded-xl border border-slate-800">
              <span class="text-slate-400 block mb-1">Packaging Box</span>
              <span class="font-bold text-slate-200">{{ product.dimensions || 'Standard' }}</span>
            </div>
          </div>

          <!-- DIGITAL DOWNLOAD SPECIFICATIONS -->
          <div v-if="product.product_type === 'DIGITAL'" class="space-y-3 text-xs">
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
              <div class="bg-slate-900/60 p-3 rounded-xl border border-slate-800">
                <span class="text-slate-400 block mb-1">File Container</span>
                <span class="font-bold text-cyan-400">{{ product.file_format }}</span>
              </div>
              <div class="bg-slate-900/60 p-3 rounded-xl border border-slate-800">
                <span class="text-slate-400 block mb-1">Asset Size</span>
                <span class="font-bold text-slate-200">{{ product.file_size_mb }} MB</span>
              </div>
              <div class="bg-slate-900/60 p-3 rounded-xl border border-slate-800">
                <span class="text-slate-400 block mb-1">License Scope</span>
                <span class="font-bold text-slate-200">{{ product.license_type || 'Commercial' }}</span>
              </div>
            </div>
            <div class="p-3 bg-cyan-950/30 border border-cyan-800/40 rounded-xl text-cyan-200 flex items-center space-x-2">
              <span>⚡</span>
              <span>Instant download link and secure cryptographic access token generated on order completion.</span>
            </div>
          </div>

          <!-- SAAS TIER SPECIFICATIONS -->
          <div v-if="product.product_type === 'SAAS'" class="space-y-3 text-xs">
            <div class="flex items-center justify-between bg-slate-900/60 p-3 rounded-xl border border-slate-800">
              <div>
                <span class="font-bold text-amber-400">{{ product.tier_level || 'Pro Tier' }}</span>
                <span class="text-slate-400 ml-2">({{ product.trial_period_days }}-Day Risk-Free Trial Included)</span>
              </div>
              <span class="font-bold text-white uppercase">{{ product.billing_interval }} billing</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <div
                v-for="(feature, idx) in (product.features_list || ['Full API access', 'Priority support', 'Daily backups'])"
                :key="idx"
                class="flex items-center space-x-2 bg-slate-900/40 p-2.5 rounded-lg border border-slate-800/80 text-slate-300"
              >
                <span class="text-emerald-400">✓</span>
                <span>{{ feature }}</span>
              </div>
            </div>
          </div>

          <!-- COURSE SYLLABUS SPECIFICATIONS -->
          <div v-if="product.product_type === 'COURSE'" class="space-y-3 text-xs">
            <div class="flex items-center space-x-3 bg-slate-900/60 p-3 rounded-xl border border-slate-800">
              <div class="w-10 h-10 rounded-full bg-purple-600/30 flex items-center justify-center text-lg">
                🎓
              </div>
              <div>
                <span class="font-bold text-white">{{ product.instructor_name || 'Senior Instructor' }}</span>
                <p class="text-[11px] text-slate-400">{{ product.instructor_title }}</p>
              </div>
            </div>
            <div v-if="product.syllabus" class="space-y-2 mt-2">
              <span class="font-bold text-slate-300 block">Course Syllabus:</span>
              <div
                v-for="(mod, i) in product.syllabus"
                :key="i"
                class="bg-slate-900/50 p-2.5 rounded-lg border border-slate-800 flex items-center justify-between"
              >
                <span class="font-medium text-slate-200">{{ mod.module }}</span>
                <span class="text-slate-400">{{ mod.lessons }} lessons · {{ mod.duration }}</span>
              </div>
            </div>
          </div>

        </div>

      </div>

    </div>
  </div>
</template>
