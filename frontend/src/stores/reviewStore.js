import { defineStore } from 'pinia';
import { api } from '../api/client';

export const useReviewStore = defineStore('reviews', {
  state: () => ({
    reviews: [],
    isLoading: false,
    filterRating: 0, // 0 for all
    verifiedOnly: false,
    photosOnly: false,
    reviewSubmissionSuccess: false,
  }),

  getters: {
    filteredReviews: (state) => {
      return state.reviews.filter(r => {
        if (state.filterRating > 0 && r.rating !== state.filterRating) return false;
        if (state.verifiedOnly && !r.is_verified_buyer) return false;
        if (state.photosOnly && !r.photo_url) return false;
        return true;
      });
    },

    averageRating: (state) => {
      if (state.reviews.length === 0) return 5.0;
      const sum = state.reviews.reduce((acc, r) => acc + r.rating, 0);
      return (sum / state.reviews.length).toFixed(1);
    },

    ratingBreakdown: (state) => {
      const breakdown = { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 };
      state.reviews.forEach(r => {
        if (breakdown[r.rating] !== undefined) {
          breakdown[r.rating]++;
        }
      });
      const total = state.reviews.length || 1;
      return {
        counts: breakdown,
        percentages: {
          5: Math.round((breakdown[5] / total) * 100),
          4: Math.round((breakdown[4] / total) * 100),
          3: Math.round((breakdown[3] / total) * 100),
          2: Math.round((breakdown[2] / total) * 100),
          1: Math.round((breakdown[1] / total) * 100),
        }
      };
    }
  },

  actions: {
    async loadReviews(productId = null) {
      this.isLoading = true;
      try {
        const data = await api.getReviews(productId);
        this.reviews = data;
      } catch (err) {
        console.error('Failed to load reviews:', err);
      } finally {
        this.isLoading = false;
      }
    },

    addReview(newReview) {
      const reviewObj = {
        id: Date.now(),
        ...newReview,
        is_verified_buyer: true,
        helpful_votes: 0,
        created_at: new Date().toISOString()
      };
      this.reviews.unshift(reviewObj);
      this.reviewSubmissionSuccess = true;
      setTimeout(() => {
        this.reviewSubmissionSuccess = false;
      }, 4000);
    },

    voteHelpful(reviewId) {
      const target = this.reviews.find(r => r.id === reviewId);
      if (target) {
        target.helpful_votes++;
      }
    }
  }
});
