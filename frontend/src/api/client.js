import { MOCK_PRODUCTS, MOCK_REVIEWS, MOCK_AFFILIATE, CURRENCY_RATES, TAX_RATES } from '../data/mockData';

const BASE_URL = 'http://127.0.0.1:8000/api';

async function request(url, options = {}) {
  try {
    const res = await fetch(`${BASE_URL}${url}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.warn(`Backend API unavailable at ${url}, using local responsive fallback:`, err.message);
    return null;
  }
}

export const api = {
  async getProducts(params = {}) {
    const query = new URLSearchParams(params).toString();
    const data = await request(`/products/?${query}`);
    if (data && data.results) return data.results;
    if (data && Array.isArray(data)) return data;

    // Fallback: local filter
    let results = [...MOCK_PRODUCTS];
    if (params.type && params.type !== 'ALL') {
      results = results.filter(p => p.product_type === params.type);
    }
    if (params.search) {
      const q = params.search.toLowerCase();
      results = results.filter(p => p.name.toLowerCase().includes(q) || p.short_description.toLowerCase().includes(q));
    }
    if (params.sort === 'price_asc') {
      results.sort((a, b) => a.price - b.price);
    } else if (params.sort === 'price_desc') {
      results.sort((a, b) => b.price - a.price);
    } else if (params.sort === 'rating') {
      results.sort((a, b) => b.rating_average - a.rating_average);
    }
    return results;
  },

  async verifyCoupon(code, subtotal) {
    const data = await request('/orders/coupon/verify/', {
      method: 'POST',
      body: JSON.stringify({ code, subtotal })
    });
    if (data) return data;

    // Fallback logic
    const clean = code.toUpperCase().trim();
    if (clean === 'SAVE20') {
      return { valid: true, code: 'SAVE20', discount_usd: Math.round(subtotal * 0.20 * 100) / 100, message: '20% Off Promo Code Applied!' };
    }
    if (clean === 'DIGITAL50') {
      return { valid: true, code: 'DIGITAL50', discount_usd: Math.round(subtotal * 0.50 * 100) / 100, message: '50% Off Digital Pass Applied!' };
    }
    if (clean === 'FREESHIP') {
      return { valid: true, code: 'FREESHIP', discount_usd: 0, free_shipping: true, message: 'Free Shipping Unlocked!' };
    }
    if (clean === 'WELCOME10') {
      const disc = Math.min(10.00, subtotal);
      return { valid: true, code: 'WELCOME10', discount_usd: disc, message: '$10.00 Welcome Discount Applied!' };
    }
    return { valid: false, message: 'Invalid promo or coupon code.' };
  },

  async calculateCheckout(payload) {
    const data = await request('/orders/calculate/', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
    if (data) return data;

    // Fallback local calculations
    const { items = [], currency = 'USD', country = 'United States', shipping_tier = 'standard', coupon_code = '' } = payload;
    const rate = CURRENCY_RATES[currency]?.rate || 1.0;
    
    let subtotal_usd = 0;
    let has_physical = false;

    items.forEach(it => {
      subtotal_usd += (it.price * (it.quantity || 1));
      if (it.product_type === 'PHYSICAL' || it.requires_shipping) has_physical = true;
    });

    const threshold = 100.00;
    const cleanCoupon = (coupon_code || '').toUpperCase().trim();
    const free_shipping_unlocked = !has_physical || subtotal_usd >= threshold || cleanCoupon === 'FREESHIP';
    const amount_needed = Math.max(0, threshold - subtotal_usd);
    const progress_percentage = Math.min(100, Math.round((subtotal_usd / threshold) * 100));

    let shipping_usd = 0;
    if (has_physical) {
      if (free_shipping_unlocked) {
        shipping_usd = shipping_tier === 'express' ? 15.00 : 0.00;
      } else {
        shipping_usd = shipping_tier === 'express' ? 25.00 : 12.00;
      }
    }

    let discount_usd = 0;
    if (cleanCoupon === 'SAVE20') discount_usd = Math.round(subtotal_usd * 0.20 * 100) / 100;
    else if (cleanCoupon === 'DIGITAL50') discount_usd = Math.round(subtotal_usd * 0.50 * 100) / 100;
    else if (cleanCoupon === 'WELCOME10') discount_usd = Math.min(10, subtotal_usd);

    const tax_rate = TAX_RATES[country] || 0.05;
    const taxable_amount = Math.max(0, subtotal_usd - discount_usd);
    const tax_usd = Math.round(taxable_amount * tax_rate * 100) / 100;
    const total_usd = Math.max(0, taxable_amount + shipping_usd + tax_usd);
    const total_in_currency = Math.round((total_usd * rate) * 10000) / 10000;

    return {
      currency,
      exchange_rate: rate,
      subtotal_usd,
      discount_usd,
      shipping_usd,
      tax_usd,
      total_usd,
      total_in_currency,
      has_physical_items: has_physical,
      free_shipping_threshold: threshold,
      free_shipping_unlocked,
      amount_needed_for_free_shipping: amount_needed,
      progress_percentage,
      tax_rate_percent: tax_rate * 100
    };
  },

  async createOrder(payload) {
    const data = await request('/orders/create/', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
    if (data) return data;

    // Fallback simulated order receipt
    const orderNumber = 'ORD-' + Math.random().toString(36).substring(2, 9).toUpperCase();
    const invoiceNumber = 'INV-' + new Date().getFullYear() + '-' + orderNumber.substring(4);
    return {
      order_number: orderNumber,
      invoice_number: invoiceNumber,
      customer_name: payload.customer_name || 'Valued Customer',
      customer_email: payload.customer_email || 'client@example.com',
      currency: payload.currency || 'USD',
      total_in_currency: payload.total_in_currency,
      total_usd: payload.total_usd,
      items: payload.items || [],
      created_at: new Date().toISOString()
    };
  },

  async getAffiliate(code = 'CREATOR25') {
    const data = await request(`/affiliates/dashboard/${code}/`);
    if (data) return data;
    return MOCK_AFFILIATE;
  },

  async getReviews(productId = null) {
    const url = productId ? `/reviews/?product=${productId}` : '/reviews/';
    const data = await request(url);
    if (data && data.results) return data.results;
    if (data && Array.isArray(data)) return data;

    if (productId) {
      return MOCK_REVIEWS.filter(r => r.product_id === Number(productId));
    }
    return MOCK_REVIEWS;
  }
};
