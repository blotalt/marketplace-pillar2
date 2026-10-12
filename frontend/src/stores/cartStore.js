import { defineStore } from 'pinia';
import { CURRENCY_RATES } from '../data/mockData';
import { api } from '../api/client';

export const useCartStore = defineStore('cart', {
  state: () => ({
    isOpen: false,
    items: [
      // Preload with 2 sample items to immediately demo the cart features
      {
        id: 1,
        name: 'Apex MechPro Wireless Split Keyboard',
        product_type: 'PHYSICAL',
        price: 189.00,
        quantity: 1,
        image_url: 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=400&q=80',
        requires_shipping: true,
      },
      {
        id: 4,
        name: 'Cinematic 8K Color Grading LUTs & Grain Pack',
        product_type: 'DIGITAL',
        price: 39.00,
        quantity: 1,
        image_url: 'https://images.unsplash.com/photo-1536240478700-b869070f9279?auto=format&fit=crop&w=400&q=80',
        requires_shipping: false,
      }
    ],
    currency: 'USD',
    country: 'United States',
    shippingTier: 'standard',
    couponCode: '',
    couponDiscountUsd: 0,
    couponMessage: '',
    couponValid: false,
    calculation: null,
    isCalculating: false,
    isCheckoutModalOpen: false,
    lastCompletedOrder: null,
  }),

  getters: {
    itemCount: (state) => state.items.reduce((sum, it) => sum + it.quantity, 0),
    
    currencyMeta: (state) => CURRENCY_RATES[state.currency] || CURRENCY_RATES.USD,
    
    subtotalUsd: (state) => {
      return state.items.reduce((acc, it) => acc + (it.price * it.quantity), 0);
    },

    formatCurrency: (state) => {
      return (amountUsd) => {
        const meta = CURRENCY_RATES[state.currency] || CURRENCY_RATES.USD;
        const converted = amountUsd * meta.rate;
        if (state.currency === 'BTC' || state.currency === 'ETH') {
          return `${meta.symbol} ${converted.toFixed(meta.precision)}`;
        }
        if (state.currency === 'JPY') {
          return `${meta.symbol} ${Math.round(converted).toLocaleString()}`;
        }
        return `${meta.symbol} ${converted.toFixed(2)}`;
      };
    },

    freeShippingThreshold: () => 100.00,

    hasPhysicalGoods: (state) => {
      return state.items.some(it => it.product_type === 'PHYSICAL' || it.requires_shipping);
    },

    freeShippingProgress: (state) => {
      if (!state.hasPhysicalGoods) return 100;
      const subtotal = state.items.reduce((sum, it) => sum + (it.price * it.quantity), 0);
      return Math.min(100, Math.round((subtotal / 100.00) * 100));
    },

    amountForFreeShipping: (state) => {
      const subtotal = state.items.reduce((sum, it) => sum + (it.price * it.quantity), 0);
      return Math.max(0, 100.00 - subtotal);
    },

    freeShippingUnlocked: (state) => {
      if (!state.hasPhysicalGoods) return true;
      if (state.couponCode.toUpperCase() === 'FREESHIP') return true;
      const subtotal = state.items.reduce((sum, it) => sum + (it.price * it.quantity), 0);
      return subtotal >= 100.00;
    }
  },

  actions: {
    openCart() {
      this.isOpen = true;
      this.recalculate();
    },

    closeCart() {
      this.isOpen = false;
    },

    toggleCart() {
      this.isOpen = !this.isOpen;
      if (this.isOpen) this.recalculate();
    },

    setCurrency(currencyCode) {
      this.currency = currencyCode;
      this.recalculate();
    },

    setCountry(countryName) {
      this.country = countryName;
      this.recalculate();
    },

    setShippingTier(tier) {
      this.shippingTier = tier;
      this.recalculate();
    },

    addItem(product, quantity = 1) {
      const existing = this.items.find(i => i.id === product.id);
      if (existing) {
        existing.quantity += quantity;
      } else {
        this.items.push({
          id: product.id,
          name: product.name,
          product_type: product.product_type,
          price: Number(product.price),
          quantity: quantity,
          image_url: product.image_url,
          requires_shipping: product.requires_shipping !== false,
          download_link: product.download_link,
          file_format: product.file_format,
          billing_interval: product.billing_interval
        });
      }
      this.isOpen = true;
      this.recalculate();
    },

    updateQuantity(productId, quantity) {
      const item = this.items.find(i => i.id === productId);
      if (item) {
        if (quantity <= 0) {
          this.removeItem(productId);
        } else {
          item.quantity = quantity;
          this.recalculate();
        }
      }
    },

    removeItem(productId) {
      this.items = this.items.filter(i => i.id !== productId);
      this.recalculate();
    },

    clearCart() {
      this.items = [];
      this.couponCode = '';
      this.couponDiscountUsd = 0;
      this.couponMessage = '';
      this.couponValid = false;
      this.recalculate();
    },

    async applyCoupon(code) {
      if (!code) return;
      this.isCalculating = true;
      const res = await api.verifyCoupon(code, this.subtotalUsd);
      this.couponMessage = res.message;
      this.couponValid = res.valid;
      if (res.valid) {
        this.couponCode = res.code;
        this.couponDiscountUsd = res.discount_usd || 0;
      } else {
        this.couponDiscountUsd = 0;
      }
      this.isCalculating = false;
      await this.recalculate();
    },

    removeCoupon() {
      this.couponCode = '';
      this.couponDiscountUsd = 0;
      this.couponMessage = '';
      this.couponValid = false;
      this.recalculate();
    },

    async recalculate() {
      this.isCalculating = true;
      const payload = {
        items: this.items,
        currency: this.currency,
        country: this.country,
        shipping_tier: this.shippingTier,
        coupon_code: this.couponCode,
      };
      const res = await api.calculateCheckout(payload);
      this.calculation = res;
      this.isCalculating = false;
    },

    openCheckout() {
      this.isOpen = false;
      this.isCheckoutModalOpen = true;
    },

    closeCheckout() {
      this.isCheckoutModalOpen = false;
    },

    async processOrder(customerDetails) {
      const payload = {
        items: this.items,
        currency: this.currency,
        customer_name: customerDetails.name,
        customer_email: customerDetails.email,
        customer_country: this.country,
        shipping_address: customerDetails.address,
        payment_method: customerDetails.paymentMethod,
        referral_code: customerDetails.referralCode || '',
        coupon_code: this.couponCode,
        subtotal_usd: this.calculation?.subtotal_usd || this.subtotalUsd,
        discount_usd: this.calculation?.discount_usd || 0,
        shipping_usd: this.calculation?.shipping_usd || 0,
        tax_usd: this.calculation?.tax_usd || 0,
        total_usd: this.calculation?.total_usd || this.subtotalUsd,
        total_in_currency: this.calculation?.total_in_currency || this.subtotalUsd,
      };

      const result = await api.createOrder(payload);
      this.lastCompletedOrder = result;
      this.clearCart();
      return result;
    }
  }
});
