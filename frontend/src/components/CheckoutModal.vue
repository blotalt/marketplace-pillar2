<script setup>
import { ref } from 'vue';
import { useCartStore } from '../stores/cartStore';

const emit = defineEmits(['order-success']);

const cartStore = useCartStore();

const customerName = ref('Alex Morgan');
const customerEmail = ref('alex.morgan@techventures.io');
const shippingAddress = ref('742 Evergreen Terrace, San Francisco, CA');
const referralCode = ref('CREATOR25');
const paymentMethod = ref('Credit Card');
const isSubmitting = ref(false);
const orderPlaced = ref(null);

async function handlePlaceOrder() {
  isSubmitting.value = true;
  try {
    const res = await cartStore.processOrder({
      name: customerName.value,
      email: customerEmail.value,
      address: shippingAddress.value,
      referralCode: referralCode.value,
      paymentMethod: paymentMethod.value,
    });
    orderPlaced.value = res;
    emit('order-success', res);
  } catch (err) {
    console.error('Order error:', err);
  } finally {
    isSubmitting.value = false;
  }
}

function close() {
  orderPlaced.value = null;
  cartStore.closeCheckout();
}
</script>

<template>
  <div v-if="cartStore.isCheckoutModalOpen" class="fixed inset-0 z-50 overflow-y-auto flex items-center justify-center p-4 sm:p-6">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-slate-950/80 backdrop-blur-md" @click="close"></div>

    <div class="relative bg-slate-900 border border-slate-700/80 rounded-3xl max-w-2xl w-full shadow-2xl overflow-hidden z-10 max-h-[90vh] flex flex-col">
      
      <!-- Modal Header -->
      <div class="p-6 border-b border-slate-800 flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <span class="text-2xl">⚡</span>
          <div>
            <h3 class="text-lg font-bold text-white">Instant Checkout</h3>
            <p class="text-xs text-slate-400">Currency: {{ cartStore.currency }} · Secure 256-bit SSL</p>
          </div>
        </div>
        <button @click="close" class="text-slate-400 hover:text-white text-lg">✕</button>
      </div>

      <!-- SUCCESS CONFIRMATION STATE -->
      <div v-if="orderPlaced" class="p-8 space-y-6 text-center overflow-y-auto">
        <div class="w-16 h-16 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mx-auto flex items-center justify-center text-3xl">
          ✓
        </div>
        <div>
          <span class="text-xs uppercase tracking-wider text-emerald-400 font-bold">Payment Verified & Settled</span>
          <h2 class="text-2xl font-extrabold text-white mt-1">Thank you for your order!</h2>
          <p class="text-xs text-slate-400 mt-1">
            Order Reference: <strong class="font-mono text-slate-200">{{ orderPlaced.order_number }}</strong>
          </p>
        </div>

        <!-- Digital Assets Access Box -->
        <div class="bg-slate-800/80 rounded-2xl p-4 border border-slate-700 text-left space-y-2">
          <h4 class="text-xs font-bold text-white uppercase tracking-wider">📦 Instant Access & Digital Entitlements</h4>
          <p class="text-xs text-slate-300">
            Digital files, licenses, and course modules have been provisioned to <strong>{{ customerEmail }}</strong>.
          </p>
          <div class="pt-2 flex flex-wrap gap-2 text-xs">
            <span class="bg-indigo-950/80 text-indigo-300 px-3 py-1.5 rounded-lg border border-indigo-800 font-mono">
              🔑 Token: KEY-{{ Math.random().toString(36).substring(2, 10).toUpperCase() }}
            </span>
            <span class="bg-slate-900 text-slate-300 px-3 py-1.5 rounded-lg border border-slate-800">
              ⚡ Download Expiry: 72 Hours
            </span>
          </div>
        </div>

        <!-- Action CTAs -->
        <div class="flex flex-col sm:flex-row gap-3 pt-2">
          <button
            @click="$emit('view-invoice', orderPlaced); close();"
            class="flex-1 py-3 px-4 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg transition-transform active:scale-95 flex items-center justify-center space-x-1"
          >
            <span>🧾 View & Download PDF Invoice</span>
          </button>
          <button
            @click="close"
            class="py-3 px-4 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs rounded-xl"
          >
            Continue Shopping
          </button>
        </div>
      </div>

      <!-- CHECKOUT FORM STATE -->
      <div v-else class="overflow-y-auto p-6 space-y-6">
        
        <!-- Contact & Delivery -->
        <div class="space-y-4">
          <h4 class="text-xs font-bold text-slate-300 uppercase tracking-wider">1. Contact & Delivery Info</h4>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div>
              <label class="block text-slate-400 mb-1">Full Name</label>
              <input
                type="text"
                v-model="customerName"
                class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-white focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
            </div>
            <div>
              <label class="block text-slate-400 mb-1">Email (for receipts & downloads)</label>
              <input
                type="email"
                v-model="customerEmail"
                class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-white focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
            </div>
          </div>

          <div v-if="cartStore.hasPhysicalGoods" class="text-xs">
            <label class="block text-slate-400 mb-1">Shipping Address (Physical Goods)</label>
            <input
              type="text"
              v-model="shippingAddress"
              class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-white focus:outline-none focus:ring-1 focus:ring-indigo-500"
            />
          </div>
        </div>

        <!-- Affiliate Code Field -->
        <div class="pt-2 border-t border-slate-800 text-xs">
          <label class="block text-slate-400 mb-1">Referral / Affiliate Code (optional)</label>
          <input
            type="text"
            v-model="referralCode"
            placeholder="CREATOR25"
            class="w-full sm:w-1/2 bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-white uppercase font-mono focus:outline-none focus:ring-1 focus:ring-indigo-500"
          />
        </div>

        <!-- Payment Method Selection -->
        <div class="pt-2 border-t border-slate-800 space-y-3">
          <h4 class="text-xs font-bold text-slate-300 uppercase tracking-wider">2. Payment Gateway</h4>
          
          <div class="grid grid-cols-3 gap-3 text-xs">
            <button
              @click="paymentMethod = 'Credit Card'"
              :class="[
                'p-3 rounded-xl border font-semibold flex flex-col items-center justify-center space-y-1 transition-all',
                paymentMethod === 'Credit Card' ? 'border-indigo-500 bg-indigo-500/10 text-white' : 'border-slate-800 bg-slate-800/60 text-slate-400'
              ]"
            >
              <span class="text-lg">💳</span>
              <span>Credit Card</span>
            </button>
            <button
              @click="paymentMethod = 'Crypto'"
              :class="[
                'p-3 rounded-xl border font-semibold flex flex-col items-center justify-center space-y-1 transition-all',
                paymentMethod === 'Crypto' ? 'border-indigo-500 bg-indigo-500/10 text-white' : 'border-slate-800 bg-slate-800/60 text-slate-400'
              ]"
            >
              <span class="text-lg">🪙</span>
              <span>Crypto Pay</span>
            </button>
            <button
              @click="paymentMethod = 'PayPal'"
              :class="[
                'p-3 rounded-xl border font-semibold flex flex-col items-center justify-center space-y-1 transition-all',
                paymentMethod === 'PayPal' ? 'border-indigo-500 bg-indigo-500/10 text-white' : 'border-slate-800 bg-slate-800/60 text-slate-400'
              ]"
            >
              <span class="text-lg">🅿️</span>
              <span>PayPal</span>
            </button>
          </div>

          <!-- Mock Payment details -->
          <div v-if="paymentMethod === 'Credit Card'" class="p-3 bg-slate-800/50 rounded-xl border border-slate-700 text-xs space-y-2">
            <input
              type="text"
              readonly
              value="•••• •••• •••• 4242 (Simulated Test Card)"
              class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-300 font-mono text-xs"
            />
          </div>
          <div v-else-if="paymentMethod === 'Crypto'" class="p-3 bg-slate-800/50 rounded-xl border border-slate-700 text-xs text-slate-300 space-y-1">
            <p>Direct Web3 Deposit ready. Supported: BTC, ETH, USDT on Ethereum & Polygon.</p>
          </div>
          <div v-else class="p-3 bg-slate-800/50 rounded-xl border border-slate-700 text-xs text-slate-300">
            <p>One-click redirection to PayPal sandbox gateway configured.</p>
          </div>
        </div>

        <!-- Summary & Final Submit -->
        <div class="pt-4 border-t border-slate-800 space-y-3">
          <div class="flex items-center justify-between text-sm font-extrabold text-white">
            <span>Amount to charge ({{ cartStore.currency }}):</span>
            <span class="text-xl text-indigo-400">
              {{ cartStore.formatCurrency(cartStore.calculation?.total_usd ?? cartStore.subtotalUsd) }}
            </span>
          </div>

          <button
            @click="handlePlaceOrder"
            :disabled="isSubmitting"
            class="w-full py-4 bg-indigo-600 hover:bg-indigo-500 text-white font-extrabold text-sm rounded-xl shadow-xl shadow-indigo-600/30 transition-all active:scale-95 disabled:opacity-50 flex items-center justify-center space-x-2"
          >
            <span v-if="isSubmitting">Processing Transaction... ⏳</span>
            <span v-else>Authorize & Complete Purchase ⚡</span>
          </button>
        </div>

      </div>

    </div>
  </div>
</template>
