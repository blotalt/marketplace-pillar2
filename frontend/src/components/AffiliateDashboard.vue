<script setup>
import { onMounted, ref } from 'vue';
import { useAffiliateStore } from '../stores/affiliateStore';

const affiliateStore = useAffiliateStore();
const selectedPayoutMethod = ref('PayPal');

onMounted(() => {
  affiliateStore.loadAffiliate();
});

function handlePayout() {
  affiliateStore.requestPayout(selectedPayoutMethod.value);
}
</script>

<template>
  <div class="space-y-8">
    
    <!-- Header banner -->
    <div class="bg-gradient-to-r from-indigo-950 via-slate-900 to-purple-950 p-6 sm:p-8 rounded-3xl border border-indigo-900/50 flex flex-col md:flex-row justify-between items-start md:items-center gap-6 shadow-xl">
      <div>
        <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-bold uppercase tracking-wide mb-3 border border-indigo-500/30">
          <span>🤝 Affiliate Partner Portal</span>
        </div>
        <h2 class="text-2xl sm:text-3xl font-extrabold text-white">
          {{ affiliateStore.affiliateData?.user_name || 'Alex River (Creator)' }}
        </h2>
        <p class="text-xs sm:text-sm text-slate-400 mt-1">
          Standard Partner Tier: <strong class="text-emerald-400 font-bold">{{ affiliateStore.affiliateData?.commission_rate || 15 }}% Commission</strong> on all referred hardware, digital downloads, SaaS, and course sales.
        </p>
      </div>

      <!-- Payout Request Button -->
      <div class="bg-slate-900/80 p-4 rounded-2xl border border-slate-800 flex flex-col sm:flex-row items-center gap-3 w-full md:w-auto">
        <div>
          <span class="text-[11px] text-slate-400 block">Available Balance:</span>
          <span class="text-xl font-extrabold text-emerald-400 font-mono">
            ${{ affiliateStore.affiliateData?.balance_payable_usd?.toFixed(2) || '0.00' }}
          </span>
        </div>
        <select
          v-model="selectedPayoutMethod"
          class="bg-slate-800 text-xs font-semibold text-slate-200 rounded-xl px-2.5 py-2 border border-slate-700"
        >
          <option value="PayPal">PayPal</option>
          <option value="Wise">Wise Wire</option>
          <option value="USDT">Crypto (USDT)</option>
        </select>
        <button
          @click="handlePayout"
          :disabled="!affiliateStore.affiliateData || affiliateStore.affiliateData.balance_payable_usd <= 0"
          class="w-full sm:w-auto px-4 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 text-white font-bold text-xs rounded-xl shadow-lg transition-transform active:scale-95 whitespace-nowrap"
        >
          Request Payout 💸
        </button>
      </div>
    </div>

    <!-- Payout Notification Alert -->
    <div v-if="affiliateStore.payoutSuccessMsg" class="bg-emerald-950/60 border border-emerald-500/50 p-4 rounded-2xl text-emerald-300 text-xs flex items-center space-x-2">
      <span>✓</span>
      <span>{{ affiliateStore.payoutSuccessMsg }}</span>
    </div>

    <!-- Referral Link Box -->
    <div class="bg-slate-800/60 p-6 rounded-2xl border border-slate-700/60 space-y-3">
      <h3 class="text-xs font-bold text-slate-300 uppercase tracking-wider">Your Personalized Referral Link</h3>
      <div class="flex flex-col sm:flex-row items-center gap-3">
        <div class="relative flex-1 w-full">
          <input
            type="text"
            readonly
            :value="affiliateStore.referralLink"
            class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white font-mono text-xs focus:outline-none"
          />
        </div>
        <button
          @click="affiliateStore.copyLinkToClipboard"
          class="w-full sm:w-auto px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-indigo-600/25 flex items-center justify-center space-x-2 transition-transform active:scale-95"
        >
          <span>{{ affiliateStore.copyNotification ? 'Copied to Clipboard! ✓' : 'Copy Referral Link 📋' }}</span>
        </button>
      </div>
      <p class="text-[11px] text-slate-500">
        Cookies track visitor referral credit for 60 days. Commissions are credited immediately once an order is settled.
      </p>
    </div>

    <!-- Analytics KPI Cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="bg-slate-800/70 p-5 rounded-2xl border border-slate-700/60">
        <span class="text-xs text-slate-400 block mb-1">Total Link Clicks</span>
        <span class="text-2xl font-extrabold text-white font-mono">
          {{ affiliateStore.affiliateData?.total_clicks?.toLocaleString() || '1,840' }}
        </span>
        <span class="text-[11px] text-emerald-400 block mt-1">↑ +14.2% traffic</span>
      </div>

      <div class="bg-slate-800/70 p-5 rounded-2xl border border-slate-700/60">
        <span class="text-xs text-slate-400 block mb-1">Referred Orders</span>
        <span class="text-2xl font-extrabold text-white font-mono">
          {{ affiliateStore.affiliateData?.total_sales_count || 142 }}
        </span>
        <span class="text-[11px] text-indigo-400 block mt-1">Verified checkouts</span>
      </div>

      <div class="bg-slate-800/70 p-5 rounded-2xl border border-slate-700/60">
        <span class="text-xs text-slate-400 block mb-1">Conversion Rate</span>
        <span class="text-2xl font-extrabold text-cyan-400 font-mono">
          {{ affiliateStore.conversionRate }}
        </span>
        <span class="text-[11px] text-cyan-500 block mt-1">Clicks to orders ratio</span>
      </div>

      <div class="bg-slate-800/70 p-5 rounded-2xl border border-slate-700/60">
        <span class="text-xs text-slate-400 block mb-1">Gross Earnings</span>
        <span class="text-2xl font-extrabold text-emerald-400 font-mono">
          ${{ affiliateStore.affiliateData?.total_earnings_usd?.toFixed(2) || '3,420.00' }}
        </span>
        <span class="text-[11px] text-slate-400 block mt-1">All-time commissions</span>
      </div>
    </div>

    <!-- Interactive Conversion Analytics Graph Visualizer -->
    <div class="bg-slate-800/60 p-6 rounded-2xl border border-slate-700/60 space-y-4">
      <div class="flex items-center justify-between">
        <h3 class="text-sm font-bold text-white uppercase tracking-wider">Weekly Conversion Velocity</h3>
        <span class="text-xs text-slate-400">Past 4 Weeks Performance</span>
      </div>

      <div class="grid grid-cols-4 gap-4 pt-4">
        <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800 space-y-2">
          <div class="flex justify-between text-xs text-slate-400">
            <span>Week 1</span>
            <span class="text-emerald-400 font-bold">$780.00</span>
          </div>
          <div class="h-16 flex items-end">
            <div class="w-full bg-indigo-600 rounded-t h-[65%]"></div>
          </div>
          <span class="text-[10px] text-slate-500 block text-center">412 clicks · 31 orders</span>
        </div>

        <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800 space-y-2">
          <div class="flex justify-between text-xs text-slate-400">
            <span>Week 2</span>
            <span class="text-emerald-400 font-bold">$920.00</span>
          </div>
          <div class="h-16 flex items-end">
            <div class="w-full bg-indigo-600 rounded-t h-[80%]"></div>
          </div>
          <span class="text-[10px] text-slate-500 block text-center">485 clicks · 38 orders</span>
        </div>

        <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800 space-y-2">
          <div class="flex justify-between text-xs text-slate-400">
            <span>Week 3</span>
            <span class="text-emerald-400 font-bold">$610.00</span>
          </div>
          <div class="h-16 flex items-end">
            <div class="w-full bg-indigo-600 rounded-t h-[50%]"></div>
          </div>
          <span class="text-[10px] text-slate-500 block text-center">360 clicks · 26 orders</span>
        </div>

        <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800 space-y-2">
          <div class="flex justify-between text-xs text-slate-400">
            <span>Week 4 (Current)</span>
            <span class="text-emerald-400 font-bold">$1,110.00</span>
          </div>
          <div class="h-16 flex items-end">
            <div class="w-full bg-gradient-to-t from-indigo-600 to-purple-500 rounded-t h-[100%]"></div>
          </div>
          <span class="text-[10px] text-slate-500 block text-center">583 clicks · 47 orders</span>
        </div>
      </div>
    </div>

    <!-- Referral Order History Table -->
    <div class="bg-slate-800/60 p-6 rounded-2xl border border-slate-700/60 space-y-4">
      <h3 class="text-sm font-bold text-white uppercase tracking-wider">Recent Referral Conversions</h3>
      
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead>
            <tr class="border-b border-slate-700 text-slate-400 font-semibold">
              <th class="py-3 px-3">Order ID</th>
              <th class="py-3 px-3">Sale Total</th>
              <th class="py-3 px-3">Commission (15%)</th>
              <th class="py-3 px-3">Status</th>
              <th class="py-3 px-3">Date</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800 text-slate-300">
            <tr v-for="ref in affiliateStore.affiliateData?.referrals" :key="ref.id" class="hover:bg-slate-700/30">
              <td class="py-3 px-3 font-mono font-bold text-white">{{ ref.order_number }}</td>
              <td class="py-3 px-3 font-mono">${{ ref.order_total_usd.toFixed(2) }}</td>
              <td class="py-3 px-3 font-mono font-bold text-emerald-400">+${{ ref.commission_amount_usd.toFixed(2) }}</td>
              <td class="py-3 px-3">
                <span
                  :class="[
                    'px-2 py-0.5 rounded text-[10px] font-bold uppercase',
                    ref.status === 'paid' ? 'bg-cyan-500/10 text-cyan-400' : 'bg-emerald-500/10 text-emerald-400'
                  ]"
                >
                  {{ ref.status }}
                </span>
              </td>
              <td class="py-3 px-3 text-slate-400">{{ ref.created_at }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>
