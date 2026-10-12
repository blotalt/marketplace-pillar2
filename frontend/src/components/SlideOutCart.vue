<script setup>
import { ref } from 'vue';
import { useCartStore } from '../stores/cartStore';
import { CURRENCY_RATES, TAX_RATES } from '../data/mockData';

const cartStore = useCartStore();
const couponInput = ref('');
const countries = Object.keys(TAX_RATES);

function applyCoupon() {
  if (couponInput.value.trim()) {
    cartStore.applyCoupon(couponInput.value.trim());
  }
}

function quickApply(code) {
  couponInput.value = code;
  cartStore.applyCoupon(code);
}
</script>

<template>
  <div v-if="cartStore.isOpen" class="fixed inset-0 z-50 overflow-hidden">
    <!-- Backdrop -->
    <div
      class="fixed inset-0 bg-slate-950/70 backdrop-blur-sm transition-opacity duration-300"
      @click="cartStore.closeCart()"
    ></div>

    <div class="fixed inset-y-0 right-0 max-w-full flex pl-10">
      <div class="w-screen max-w-md bg-slate-900 border-l border-slate-800 shadow-2xl flex flex-col justify-between">
        
        <!-- Cart Header -->
        <div class="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-900/90">
          <div class="flex items-center space-x-2">
            <span class="text-xl">🛒</span>
            <h2 class="text-lg font-extrabold text-white">Your Universal Cart</h2>
            <span class="text-xs bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded-full font-bold">
              {{ cartStore.itemCount }}
            </span>
          </div>

          <div class="flex items-center space-x-3">
            <!-- Currency selector inside cart -->
            <select
              :value="cartStore.currency"
              @change="cartStore.setCurrency($event.target.value)"
              class="bg-slate-800 text-xs font-bold text-slate-200 rounded-lg px-2.5 py-1.5 border border-slate-700 cursor-pointer"
            >
              <option v-for="c in Object.values(CURRENCY_RATES)" :key="c.code" :value="c.code">
                {{ c.code }} ({{ c.symbol }})
              </option>
            </select>

            <button
              @click="cartStore.closeCart()"
              class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center transition-colors"
            >
              ✕
            </button>
          </div>
        </div>

        <!-- Tiered Free Shipping & Discount Progress Bar -->
        <div class="px-5 py-3 bg-slate-800/40 border-b border-slate-800">
          <div v-if="cartStore.hasPhysicalGoods">
            <div class="flex justify-between text-xs mb-1.5">
              <span v-if="cartStore.freeShippingUnlocked" class="text-emerald-400 font-bold flex items-center space-x-1">
                <span>🎉</span>
                <span>FREE Shipping Unlocked!</span>
              </span>
              <span v-else class="text-slate-300 font-medium">
                Add <strong class="text-indigo-400">{{ cartStore.formatCurrency(cartStore.amountForFreeShipping) }}</strong> for Free Shipping!
              </span>
              <span class="text-[11px] font-bold text-slate-400">{{ cartStore.freeShippingProgress }}%</span>
            </div>

            <!-- Progress Meter -->
            <div class="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
              <div
                class="h-full bg-gradient-to-r from-indigo-500 via-purple-500 to-emerald-400 transition-all duration-500"
                :style="{ width: `${cartStore.freeShippingProgress}%` }"
              ></div>
            </div>
          </div>
          <div v-else class="text-xs text-cyan-300 flex items-center space-x-1 font-medium">
            <span>⚡</span>
            <span>Digital Assets & SaaS Tiers — Zero Shipping Fee Always!</span>
          </div>
        </div>

        <!-- Cart Items Scrollable List -->
        <div class="flex-1 overflow-y-auto p-5 space-y-4">
          <div v-if="cartStore.items.length === 0" class="text-center py-16 text-slate-400 space-y-3">
            <div class="text-4xl">🛍️</div>
            <p class="text-sm font-semibold">Your cart is empty.</p>
            <p class="text-xs text-slate-500">Discover hardware, digital kits, SaaS, and courses in the store!</p>
          </div>

          <div
            v-for="item in cartStore.items"
            :key="item.id"
            class="bg-slate-800/60 rounded-2xl p-3 border border-slate-700/60 flex space-x-3 group"
          >
            <!-- Thumbnail -->
            <img :src="item.image_url" :alt="item.name" class="w-16 h-16 rounded-xl object-cover bg-slate-900 border border-slate-700" />

            <!-- Item details -->
            <div class="flex-1 flex flex-col justify-between">
              <div>
                <div class="flex items-start justify-between">
                  <h4 class="text-xs font-bold text-white line-clamp-1 pr-2">{{ item.name }}</h4>
                  <button
                    @click="cartStore.removeItem(item.id)"
                    class="text-slate-500 hover:text-rose-400 text-xs transition-colors"
                    title="Remove item"
                  >
                    🗑️
                  </button>
                </div>
                <div class="text-[10px] text-indigo-400 uppercase font-semibold mt-0.5">
                  {{ item.product_type }}
                </div>
              </div>

              <!-- Price & Quantity Stepper -->
              <div class="flex items-center justify-between mt-2 pt-2 border-t border-slate-700/40">
                <span class="text-xs font-extrabold text-white">
                  {{ cartStore.formatCurrency(item.price * item.quantity) }}
                </span>

                <div class="flex items-center space-x-1.5 bg-slate-900 rounded-lg p-0.5 border border-slate-700">
                  <button
                    @click="cartStore.updateQuantity(item.id, item.quantity - 1)"
                    class="w-6 h-6 rounded flex items-center justify-center text-xs text-slate-400 hover:text-white hover:bg-slate-800"
                  >
                    -
                  </button>
                  <span class="text-xs font-bold text-white px-1.5">{{ item.quantity }}</span>
                  <button
                    @click="cartStore.updateQuantity(item.id, item.quantity + 1)"
                    class="w-6 h-6 rounded flex items-center justify-center text-xs text-slate-400 hover:text-white hover:bg-slate-800"
                  >
                    +
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer: Location, Promo Code & Totals -->
        <div class="p-5 bg-slate-900 border-t border-slate-800 space-y-4">
          
          <!-- Shipping / Tax Country Estimator -->
          <div class="flex items-center justify-between text-xs">
            <span class="text-slate-400">Shipping Country:</span>
            <select
              :value="cartStore.country"
              @change="cartStore.setCountry($event.target.value)"
              class="bg-slate-800 text-slate-200 text-xs rounded-lg px-2 py-1 border border-slate-700 cursor-pointer focus:outline-none"
            >
              <option v-for="c in countries" :key="c" :value="c">{{ c }}</option>
            </select>
          </div>

          <!-- Dynamic Coupon Input -->
          <div>
            <div class="flex space-x-2">
              <input
                type="text"
                v-model="couponInput"
                placeholder="Promo code (e.g. SAVE20)"
                class="flex-1 bg-slate-800 text-slate-200 text-xs px-3 py-2 rounded-xl border border-slate-700 focus:outline-none focus:ring-1 focus:ring-indigo-500 uppercase font-mono"
              />
              <button
                @click="applyCoupon"
                :disabled="cartStore.isCalculating"
                class="px-3.5 py-2 bg-slate-700 hover:bg-slate-600 text-white font-bold text-xs rounded-xl transition-colors disabled:opacity-50"
              >
                Apply
              </button>
            </div>

            <!-- Quick sample promo suggestions -->
            <div class="flex flex-wrap gap-1.5 mt-2">
              <span class="text-[10px] text-slate-500">Try codes:</span>
              <button
                @click="quickApply('SAVE20')"
                class="text-[10px] bg-slate-800 hover:bg-slate-700 text-indigo-300 font-mono px-1.5 py-0.5 rounded border border-slate-700"
              >
                SAVE20 (-20%)
              </button>
              <button
                @click="quickApply('DIGITAL50')"
                class="text-[10px] bg-slate-800 hover:bg-slate-700 text-cyan-300 font-mono px-1.5 py-0.5 rounded border border-slate-700"
              >
                DIGITAL50 (-50%)
              </button>
              <button
                @click="quickApply('FREESHIP')"
                class="text-[10px] bg-slate-800 hover:bg-slate-700 text-emerald-300 font-mono px-1.5 py-0.5 rounded border border-slate-700"
              >
                FREESHIP
              </button>
            </div>

            <!-- Coupon feedback message -->
            <div v-if="cartStore.couponMessage" class="mt-2 text-xs flex items-center justify-between">
              <span :class="cartStore.couponValid ? 'text-emerald-400 font-semibold' : 'text-rose-400'">
                {{ cartStore.couponValid ? '✓ ' : '✕ ' }}{{ cartStore.couponMessage }}
              </span>
              <button
                v-if="cartStore.couponCode"
                @click="cartStore.removeCoupon(); couponInput = '';"
                class="text-[10px] text-slate-400 hover:text-white underline"
              >
                Remove
              </button>
            </div>
          </div>

          <!-- Cost Breakdown -->
          <div class="space-y-1.5 text-xs text-slate-300 pt-2 border-t border-slate-800">
            <div class="flex justify-between">
              <span class="text-slate-400">Subtotal</span>
              <span class="font-semibold">{{ cartStore.formatCurrency(cartStore.calculation?.subtotal_usd ?? cartStore.subtotalUsd) }}</span>
            </div>

            <div v-if="cartStore.calculation?.discount_usd > 0" class="flex justify-between text-emerald-400">
              <span>Coupon Discount ({{ cartStore.couponCode }})</span>
              <span>-{{ cartStore.formatCurrency(cartStore.calculation.discount_usd) }}</span>
            </div>

            <div v-if="cartStore.hasPhysicalGoods" class="flex justify-between">
              <span class="text-slate-400">Shipping ({{ cartStore.shippingTier }})</span>
              <span :class="cartStore.calculation?.shipping_usd === 0 ? 'text-emerald-400 font-bold' : ''">
                {{ cartStore.calculation?.shipping_usd === 0 ? 'FREE' : cartStore.formatCurrency(cartStore.calculation?.shipping_usd || 12.00) }}
              </span>
            </div>

            <div class="flex justify-between">
              <span class="text-slate-400">Estimated Tax ({{ cartStore.country }})</span>
              <span>{{ cartStore.formatCurrency(cartStore.calculation?.tax_usd || 0) }}</span>
            </div>

            <div class="flex justify-between text-sm font-extrabold text-white pt-2 border-t border-slate-800">
              <span>Total in {{ cartStore.currency }}</span>
              <span class="text-base text-indigo-400">
                {{ cartStore.formatCurrency(cartStore.calculation?.total_usd ?? cartStore.subtotalUsd) }}
              </span>
            </div>
          </div>

          <!-- Instant Checkout CTA -->
          <button
            @click="cartStore.openCheckout()"
            :disabled="cartStore.items.length === 0"
            class="w-full py-3.5 px-4 bg-gradient-to-r from-indigo-600 via-indigo-500 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-extrabold text-sm rounded-2xl shadow-xl shadow-indigo-600/30 transition-all active:scale-95 disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            <span>Proceed to Instant Checkout</span>
            <span>⚡</span>
          </button>

        </div>

      </div>
    </div>
  </div>
</template>
