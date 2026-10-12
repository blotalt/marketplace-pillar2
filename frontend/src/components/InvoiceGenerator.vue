<script setup>
import { ref, computed } from 'vue';
import { CURRENCY_RATES } from '../data/mockData';

const props = defineProps({
  initialOrder: {
    type: Object,
    default: null
  }
});

const invoiceNumber = ref(props.initialOrder?.invoice_number || `INV-2026-` + Math.random().toString(36).substring(2, 8).toUpperCase());
const issueDate = ref(new Date().toISOString().split('T')[0]);
const dueDate = ref(new Date().toISOString().split('T')[0]);
const companyName = ref('OmniCommerce Global Inc.');
const companyTaxId = ref('US-EIN-984321789');
const companyAddress = ref('100 Tech Plaza, Suite 400, San Francisco, CA 94105, USA');

const clientName = ref(props.initialOrder?.customer_name || 'Alex Morgan');
const clientEmail = ref(props.initialOrder?.customer_email || 'alex.morgan@techventures.io');
const clientAddress = ref('742 Evergreen Terrace, San Francisco, CA 94102');

const currency = ref(props.initialOrder?.currency || 'USD');
const taxPercent = ref(8.25);
const discountAmount = ref(props.initialOrder?.discount_usd || 0.0);
const notes = ref('Thank you for your business. For support and license reactivation, contact support@omnicommerce.io.');

// Customizable Line Items
const lineItems = ref(
  props.initialOrder?.items?.map(it => ({
    description: it.product_name || it.name,
    quantity: it.quantity || 1,
    unitPrice: it.unit_price_usd || it.price || 50.0
  })) || [
    { description: 'Apex MechPro Wireless Split Keyboard (Physical)', quantity: 1, unitPrice: 189.00 },
    { description: 'Cinematic 8K Color Grading LUTs & Grain Pack (Digital License)', quantity: 1, unitPrice: 39.00 }
  ]
);

function addLineItem() {
  lineItems.value.push({
    description: 'Custom Service / Asset Item',
    quantity: 1,
    unitPrice: 50.00
  });
}

function removeLineItem(index) {
  if (lineItems.value.length > 1) {
    lineItems.value.splice(index, 1);
  }
}

const subtotal = computed(() => {
  return lineItems.value.reduce((acc, it) => acc + (Number(it.quantity) * Number(it.unitPrice)), 0);
});

const taxAmount = computed(() => {
  const taxable = Math.max(0, subtotal.value - Number(discountAmount.value));
  return Math.round((taxable * (Number(taxPercent.value) / 100)) * 100) / 100;
});

const grandTotal = computed(() => {
  const taxable = Math.max(0, subtotal.value - Number(discountAmount.value));
  return Math.max(0, taxable + taxAmount.value);
});

const currentSymbol = computed(() => {
  return CURRENCY_RATES[currency.value]?.symbol || '$';
});

function printInvoice() {
  window.print();
}
</script>

<template>
  <div class="space-y-8">
    
    <!-- Top Control Bar -->
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-slate-800/80 p-5 rounded-2xl border border-slate-700/80">
      <div>
        <h2 class="text-xl font-extrabold text-white flex items-center space-x-2">
          <span>🧾</span>
          <span>Interactive Invoice & Receipt Generator</span>
        </h2>
        <p class="text-xs text-slate-400 mt-1">
          Customize line items, tax ID, and billing details in real time. Download or print instant PDF receipts.
        </p>
      </div>

      <div class="flex items-center space-x-3 w-full sm:w-auto">
        <select
          v-model="currency"
          class="bg-slate-900 text-xs font-bold text-slate-200 rounded-xl px-3 py-2 border border-slate-700 cursor-pointer"
        >
          <option v-for="c in Object.values(CURRENCY_RATES)" :key="c.code" :value="c.code">
            {{ c.code }} ({{ c.symbol }})
          </option>
        </select>

        <button
          @click="printInvoice"
          class="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-indigo-600/25 flex items-center space-x-1.5 transition-transform active:scale-95"
        >
          <span>🖨️</span>
          <span>Download / Print PDF</span>
        </button>
      </div>
    </div>

    <!-- Main Invoice Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <!-- Left Column: Customization Controls -->
      <div class="bg-slate-800/60 p-6 rounded-2xl border border-slate-700/60 space-y-5 h-fit">
        <h3 class="text-sm font-bold text-white uppercase tracking-wider">⚙️ Invoice Settings</h3>

        <div class="space-y-3 text-xs">
          <div>
            <label class="block text-slate-400 mb-1">Invoice Number</label>
            <input
              type="text"
              v-model="invoiceNumber"
              class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white font-mono"
            />
          </div>

          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block text-slate-400 mb-1">Issue Date</label>
              <input
                type="date"
                v-model="issueDate"
                class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-white"
              />
            </div>
            <div>
              <label class="block text-slate-400 mb-1">Due Date</label>
              <input
                type="date"
                v-model="dueDate"
                class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-white"
              />
            </div>
          </div>

          <div>
            <label class="block text-slate-400 mb-1">Company / Seller Name</label>
            <input
              type="text"
              v-model="companyName"
              class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white"
            />
          </div>

          <div>
            <label class="block text-slate-400 mb-1">Tax / VAT ID</label>
            <input
              type="text"
              v-model="companyTaxId"
              class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white font-mono"
            />
          </div>

          <div>
            <label class="block text-slate-400 mb-1">Client Full Name</label>
            <input
              type="text"
              v-model="clientName"
              class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white"
            />
          </div>

          <div>
            <label class="block text-slate-400 mb-1">Client Email</label>
            <input
              type="email"
              v-model="clientEmail"
              class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white"
            />
          </div>

          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block text-slate-400 mb-1">Tax Rate (%)</label>
              <input
                type="number"
                step="0.1"
                v-model="taxPercent"
                class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-white"
              />
            </div>
            <div>
              <label class="block text-slate-400 mb-1">Discount Deduction</label>
              <input
                type="number"
                step="1"
                v-model="discountAmount"
                class="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-white"
              />
            </div>
          </div>

          <div>
            <label class="block text-slate-400 mb-1">Receipt Footer Notes</label>
            <textarea
              v-model="notes"
              rows="3"
              class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white"
            ></textarea>
          </div>
        </div>
      </div>

      <!-- Right Columns: Printable Live Paper Invoice Preview -->
      <div class="lg:col-span-2">
        <div id="printable-invoice" class="bg-white text-slate-900 p-8 sm:p-10 rounded-2xl shadow-2xl border border-slate-200 space-y-8">
          
          <!-- Invoice Header -->
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-slate-200 pb-6">
            <div>
              <div class="flex items-center space-x-2">
                <span class="w-8 h-8 rounded-lg bg-indigo-600 text-white flex items-center justify-center font-bold text-sm">
                  Ω
                </span>
                <span class="text-xl font-extrabold text-slate-900 tracking-tight">{{ companyName }}</span>
              </div>
              <p class="text-xs text-slate-500 mt-1 max-w-sm">{{ companyAddress }}</p>
              <p class="text-xs text-slate-500 mt-0.5 font-mono">Tax ID: {{ companyTaxId }}</p>
            </div>

            <div class="sm:text-right">
              <span class="inline-block bg-emerald-100 text-emerald-800 font-extrabold text-xs px-3 py-1 rounded-full uppercase tracking-wider mb-2">
                ✓ PAID & SETTLED
              </span>
              <h1 class="text-2xl font-black text-slate-900 font-mono tracking-tight">{{ invoiceNumber }}</h1>
              <p class="text-xs text-slate-500 mt-0.5">Issue Date: {{ issueDate }}</p>
            </div>
          </div>

          <!-- Bill To / Ship To -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 text-xs text-slate-700">
            <div>
              <span class="font-bold text-slate-400 uppercase tracking-wider block mb-1">Billed To:</span>
              <p class="font-bold text-sm text-slate-900">{{ clientName }}</p>
              <p class="text-slate-600">{{ clientEmail }}</p>
              <p class="text-slate-600 mt-1">{{ clientAddress }}</p>
            </div>
            <div class="sm:text-right">
              <span class="font-bold text-slate-400 uppercase tracking-wider block mb-1">Payment Method:</span>
              <p class="font-bold text-slate-900">Universal Digital Payment</p>
              <p class="text-slate-600 font-mono">Currency: {{ currency }}</p>
              <p class="text-slate-600">Settled via OmniCommerce Gateway</p>
            </div>
          </div>

          <!-- Customizable Line Items Table -->
          <div>
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs">
                <thead>
                  <tr class="border-b-2 border-slate-900 text-slate-900 font-bold uppercase tracking-wider">
                    <th class="py-3 px-2">Description / Item</th>
                    <th class="py-3 px-2 w-20 text-center">Qty</th>
                    <th class="py-3 px-2 w-28 text-right">Price ({{ currentSymbol }})</th>
                    <th class="py-3 px-2 w-28 text-right">Total ({{ currentSymbol }})</th>
                    <th class="py-3 px-2 w-10 text-center print:hidden"></th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="(item, idx) in lineItems" :key="idx" class="hover:bg-slate-50 group">
                    <td class="py-3 px-2 font-medium text-slate-800">
                      <input
                        type="text"
                        v-model="item.description"
                        class="w-full bg-transparent focus:bg-white focus:ring-1 focus:ring-indigo-500 rounded p-1 border-0"
                      />
                    </td>
                    <td class="py-3 px-2 text-center">
                      <input
                        type="number"
                        min="1"
                        v-model="item.quantity"
                        class="w-14 text-center bg-transparent focus:bg-white focus:ring-1 focus:ring-indigo-500 rounded p-1 border-0 font-semibold"
                      />
                    </td>
                    <td class="py-3 px-2 text-right">
                      <input
                        type="number"
                        step="0.01"
                        v-model="item.unitPrice"
                        class="w-20 text-right bg-transparent focus:bg-white focus:ring-1 focus:ring-indigo-500 rounded p-1 border-0 font-semibold"
                      />
                    </td>
                    <td class="py-3 px-2 text-right font-bold text-slate-900">
                      {{ (item.quantity * item.unitPrice).toFixed(2) }}
                    </td>
                    <td class="py-3 px-2 text-center print:hidden">
                      <button
                        @click="removeLineItem(idx)"
                        class="text-slate-400 hover:text-rose-600 opacity-0 group-hover:opacity-100 transition-opacity"
                        title="Delete line"
                      >
                        ✕
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Add Line Item Button -->
            <button
              @click="addLineItem"
              class="mt-3 px-3 py-1.5 text-xs font-semibold text-indigo-600 hover:text-indigo-800 border border-dashed border-indigo-300 rounded-lg hover:bg-indigo-50 transition-colors print:hidden flex items-center space-x-1"
            >
              <span>+ Add Line Item</span>
            </button>
          </div>

          <!-- Total Calculation Breakdown -->
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center pt-4 border-t border-slate-200 gap-6 text-xs">
            <div class="max-w-xs text-slate-500 space-y-2">
              <p class="italic leading-relaxed">{{ notes }}</p>
              <div class="flex items-center space-x-2 pt-2 text-[11px] font-mono text-slate-400">
                <span>🔒 SHA-256 Ledger:</span>
                <span>{{ Math.random().toString(36).substring(2, 14) }}...</span>
              </div>
            </div>

            <div class="w-full sm:w-64 space-y-2 text-slate-600">
              <div class="flex justify-between">
                <span>Subtotal:</span>
                <span class="font-semibold text-slate-900">{{ currentSymbol }} {{ subtotal.toFixed(2) }}</span>
              </div>
              <div v-if="discountAmount > 0" class="flex justify-between text-emerald-600 font-medium">
                <span>Discount:</span>
                <span>-{{ currentSymbol }} {{ Number(discountAmount).toFixed(2) }}</span>
              </div>
              <div class="flex justify-between">
                <span>Tax ({{ taxPercent }}%):</span>
                <span>{{ currentSymbol }} {{ taxAmount.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between text-base font-extrabold text-slate-900 pt-2 border-t border-slate-900">
                <span>Total Amount:</span>
                <span class="text-indigo-600 font-mono">{{ currentSymbol }} {{ grandTotal.toFixed(2) }}</span>
              </div>
            </div>
          </div>

        </div>
      </div>

    </div>

  </div>
</template>
