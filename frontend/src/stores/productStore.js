import { defineStore } from 'pinia';
import { api } from '../api/client';

export const useProductStore = defineStore('products', {
  state: () => ({
    products: [],
    isLoading: false,
    selectedType: 'ALL', // 'ALL', 'PHYSICAL', 'DIGITAL', 'SAAS', 'COURSE'
    searchQuery: '',
    sortOrder: 'featured', // 'featured', 'price_asc', 'price_desc', 'rating'
    selectedProductForModal: null,
  }),

  getters: {
    filteredProducts: (state) => {
      let list = [...state.products];
      if (state.selectedType !== 'ALL') {
        list = list.filter(p => p.product_type === state.selectedType);
      }
      if (state.searchQuery.trim()) {
        const q = state.searchQuery.toLowerCase().trim();
        list = list.filter(p =>
          p.name.toLowerCase().includes(q) ||
          (p.short_description && p.short_description.toLowerCase().includes(q)) ||
          (p.category && p.category.toLowerCase().includes(q))
        );
      }
      if (state.sortOrder === 'price_asc') {
        list.sort((a, b) => Number(a.price) - Number(b.price));
      } else if (state.sortOrder === 'price_desc') {
        list.sort((a, b) => Number(b.price) - Number(a.price));
      } else if (state.sortOrder === 'rating') {
        list.sort((a, b) => Number(b.rating_average) - Number(a.rating_average));
      }
      return list;
    },

    typeCounts: (state) => {
      const counts = { ALL: state.products.length, PHYSICAL: 0, DIGITAL: 0, SAAS: 0, COURSE: 0 };
      state.products.forEach(p => {
        if (counts[p.product_type] !== undefined) {
          counts[p.product_type]++;
        }
      });
      return counts;
    }
  },

  actions: {
    async loadProducts() {
      this.isLoading = true;
      try {
        const data = await api.getProducts({
          type: this.selectedType,
          search: this.searchQuery,
          sort: this.sortOrder
        });
        this.products = data;
      } catch (err) {
        console.error('Failed to load products:', err);
      } finally {
        this.isLoading = false;
      }
    },

    setSelectedType(type) {
      this.selectedType = type;
      this.loadProducts();
    },

    setSearchQuery(query) {
      this.searchQuery = query;
    },

    setSortOrder(order) {
      this.sortOrder = order;
      this.loadProducts();
    },

    openProductModal(product) {
      this.selectedProductForModal = product;
    },

    closeProductModal() {
      this.selectedProductForModal = null;
    }
  }
});
