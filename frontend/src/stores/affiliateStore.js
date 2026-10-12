import { defineStore } from 'pinia';
import { api } from '../api/client';

export const useAffiliateStore = defineStore('affiliate', {
  state: () => ({
    affiliateData: null,
    isLoading: false,
    customReferralCode: 'CREATOR25',
    copyNotification: false,
    payoutSuccessMsg: '',
  }),

  getters: {
    referralLink: (state) => {
      const origin = window.location.origin || 'https://omnicommerce.io';
      return `${origin}?ref=${state.customReferralCode}`;
    },
    conversionRate: (state) => {
      if (!state.affiliateData || !state.affiliateData.total_clicks) return '0.00%';
      const rate = ((state.affiliateData.total_sales_count || 4) / state.affiliateData.total_clicks) * 100;
      return `${rate.toFixed(2)}%`;
    }
  },

  actions: {
    async loadAffiliate() {
      this.isLoading = true;
      try {
        const data = await api.getAffiliate(this.customReferralCode);
        this.affiliateData = data;
      } catch (err) {
        console.error('Failed to load affiliate data:', err);
      } finally {
        this.isLoading = false;
      }
    },

    copyLinkToClipboard() {
      navigator.clipboard.writeText(this.referralLink);
      this.copyNotification = true;
      setTimeout(() => {
        this.copyNotification = false;
      }, 2500);
    },

    async requestPayout(method = 'PayPal') {
      if (!this.affiliateData || this.affiliateData.balance_payable_usd <= 0) return;
      const amt = this.affiliateData.balance_payable_usd;
      this.affiliateData.balance_payable_usd = 0;
      this.affiliateData.payouts.unshift({
        id: Date.now(),
        amount_usd: amt,
        payout_method: method,
        transaction_reference: `TX-${Math.random().toString(36).substring(2, 9).toUpperCase()}`,
        status: 'Processing',
        paid_at: new Date().toISOString().split('T')[0]
      });
      this.payoutSuccessMsg = `Payout request for $${amt.toFixed(2)} submitted successfully!`;
      setTimeout(() => {
        this.payoutSuccessMsg = '';
      }, 4000);
    }
  }
});
