<script setup>
import { ref, onMounted } from 'vue';
import { useReviewStore } from '../stores/reviewStore';
import { useProductStore } from '../stores/productStore';

const reviewStore = useReviewStore();
const productStore = useProductStore();

const showWriteModal = ref(false);

// Form state
const selectedProductId = ref(1);
const formRating = ref(5);
const formAuthorName = ref('');
const formAuthorEmail = ref('');
const formTitle = ref('');
const formComment = ref('');
const formPhotoUrl = ref('');
const previewImage = ref('');

onMounted(() => {
  reviewStore.loadReviews();
  if (productStore.products.length === 0) {
    productStore.loadProducts();
  }
});

function handlePhotoUpload(e) {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (evt) => {
      previewImage.value = evt.target.result;
      formPhotoUrl.value = evt.target.result;
    };
    reader.readAsDataURL(file);
  }
}

function submitReview() {
  if (!formAuthorName.value || !formComment.value) return;

  const p = productStore.products.find(p => p.id === Number(selectedProductId.value));

  reviewStore.addReview({
    product_id: Number(selectedProductId.value),
    product_name: p ? p.name : 'Apex MechPro Wireless Split Keyboard',
    author_name: formAuthorName.value,
    author_email: formAuthorEmail.value || 'customer@example.com',
    rating: Number(formRating.value),
    title: formTitle.value || 'Exceptional Quality',
    comment: formComment.value,
    photo_url: formPhotoUrl.value,
  });

  // Reset form
  formAuthorName.value = '';
  formAuthorEmail.value = '';
  formTitle.value = '';
  formComment.value = '';
  formPhotoUrl.value = '';
  previewImage.value = '';
  showWriteModal.value = false;
}
</script>

<template>
  <div class="space-y-8">
    
    <!-- Header banner -->
    <div class="bg-slate-800/80 p-6 sm:p-8 rounded-3xl border border-slate-700/80 flex flex-col md:flex-row justify-between items-start md:items-center gap-6 shadow-xl">
      <div>
        <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-amber-500/10 text-amber-300 text-xs font-bold uppercase tracking-wide mb-3 border border-amber-500/20">
          <span>⭐ Social Proof & Customer Review Engine</span>
        </div>
        <h2 class="text-2xl sm:text-3xl font-extrabold text-white">Verified Customer Testimonials</h2>
        <p class="text-xs sm:text-sm text-slate-400 mt-1">
          Real feedback from authenticated hardware owners, digital kit creators, and academy graduates.
        </p>
      </div>

      <button
        @click="showWriteModal = true"
        class="px-5 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-extrabold text-xs rounded-xl shadow-lg shadow-indigo-600/30 flex items-center space-x-2 transition-transform active:scale-95"
      >
        <span>✍️ Write a Review</span>
      </button>
    </div>

    <!-- Review Rating Summary & Filter Bar -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 bg-slate-800/60 p-6 rounded-2xl border border-slate-700/60">
      
      <!-- Overall Rating Score -->
      <div class="flex flex-col items-center justify-center border-b md:border-b-0 md:border-r border-slate-700/60 pb-6 md:pb-0 md:pr-6 text-center">
        <span class="text-5xl font-black text-white font-mono">{{ reviewStore.averageRating }}</span>
        <div class="flex items-center space-x-1 text-amber-400 text-lg mt-2">
          <span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>
        </div>
        <span class="text-xs text-slate-400 mt-1">Based on {{ reviewStore.reviews.length }} customer experiences</span>
      </div>

      <!-- Rating Bar Breakdown -->
      <div class="space-y-1.5 md:col-span-2 text-xs">
        <div
          v-for="star in [5, 4, 3, 2, 1]"
          :key="star"
          class="flex items-center space-x-3 cursor-pointer group"
          @click="reviewStore.filterRating = reviewStore.filterRating === star ? 0 : star"
        >
          <span class="w-8 font-bold text-slate-300 group-hover:text-amber-400">{{ star }} ★</span>
          <div class="flex-1 h-2.5 bg-slate-900 rounded-full overflow-hidden border border-slate-700">
            <div
              class="h-full bg-amber-400 transition-all duration-500 rounded-full"
              :style="{ width: `${reviewStore.ratingBreakdown.percentages[star]}%` }"
            ></div>
          </div>
          <span class="w-10 text-right text-slate-400 font-mono text-[11px]">
            {{ reviewStore.ratingBreakdown.percentages[star] }}%
          </span>
        </div>
      </div>

    </div>

    <!-- Filter Toggles -->
    <div class="flex flex-wrap items-center gap-3">
      <button
        @click="reviewStore.verifiedOnly = !reviewStore.verifiedOnly"
        :class="[
          'px-3.5 py-1.5 rounded-xl text-xs font-semibold border transition-all flex items-center space-x-1.5',
          reviewStore.verifiedOnly
            ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
            : 'bg-slate-800 text-slate-400 border-slate-700 hover:text-white'
        ]"
      >
        <span>✓</span>
        <span>Verified Buyers Only</span>
      </button>

      <button
        @click="reviewStore.photosOnly = !reviewStore.photosOnly"
        :class="[
          'px-3.5 py-1.5 rounded-xl text-xs font-semibold border transition-all flex items-center space-x-1.5',
          reviewStore.photosOnly
            ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500/40'
            : 'bg-slate-800 text-slate-400 border-slate-700 hover:text-white'
        ]"
      >
        <span>📸</span>
        <span>With Photos Only</span>
      </button>

      <button
        v-if="reviewStore.filterRating > 0 || reviewStore.verifiedOnly || reviewStore.photosOnly"
        @click="reviewStore.filterRating = 0; reviewStore.verifiedOnly = false; reviewStore.photosOnly = false;"
        class="text-xs text-indigo-400 hover:underline ml-2"
      >
        Clear filters
      </button>
    </div>

    <!-- Review Feed Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div
        v-for="review in reviewStore.filteredReviews"
        :key="review.id"
        class="bg-slate-800/70 p-6 rounded-2xl border border-slate-700/60 flex flex-col justify-between space-y-4 hover:border-slate-600 transition-colors"
      >
        <div>
          <!-- Header with stars and badge -->
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-1 text-amber-400 text-sm">
              <span v-for="s in review.rating" :key="s">★</span>
            </div>
            
            <span
              v-if="review.is_verified_buyer"
              class="inline-flex items-center space-x-1 text-[11px] font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded-full"
            >
              <span>✓</span>
              <span>Verified Buyer</span>
            </span>
          </div>

          <!-- Product attribution -->
          <div class="text-[11px] text-indigo-400 font-semibold mt-2">
            Purchased: {{ review.product_name }}
          </div>

          <!-- Title & Comment -->
          <h4 class="font-bold text-white text-base mt-1">{{ review.title }}</h4>
          <p class="text-xs text-slate-300 leading-relaxed mt-2">{{ review.comment }}</p>

          <!-- Customer photo upload preview -->
          <div v-if="review.photo_url" class="mt-4 rounded-xl overflow-hidden bg-slate-900 border border-slate-700 max-h-48 w-fit">
            <img :src="review.photo_url" alt="Customer Photo Upload" class="max-h-48 object-cover rounded-xl" />
          </div>
        </div>

        <!-- Footer: Author & Helpful voting -->
        <div class="pt-4 border-t border-slate-700/40 flex items-center justify-between text-xs text-slate-400">
          <div>
            <span class="font-bold text-slate-200">{{ review.author_name }}</span>
            <span class="text-slate-500 ml-1">· {{ new Date(review.created_at).toLocaleDateString() }}</span>
          </div>

          <button
            @click="reviewStore.voteHelpful(review.id)"
            class="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-700 text-slate-300 font-medium text-xs flex items-center space-x-1 border border-slate-800 transition-colors active:scale-95"
          >
            <span>👍 Helpful</span>
            <span class="font-bold font-mono">({{ review.helpful_votes }})</span>
          </button>
        </div>
      </div>
    </div>

    <!-- WRITE REVIEW MODAL -->
    <div v-if="showWriteModal" class="fixed inset-0 z-50 overflow-y-auto flex items-center justify-center p-4">
      <div class="fixed inset-0 bg-slate-950/80 backdrop-blur-md" @click="showWriteModal = false"></div>

      <div class="relative bg-slate-900 border border-slate-700 rounded-3xl max-w-lg w-full p-6 sm:p-8 space-y-5 z-10 shadow-2xl">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-bold text-white">Write a Customer Review</h3>
          <button @click="showWriteModal = false" class="text-slate-400 hover:text-white">✕</button>
        </div>

        <div class="space-y-4 text-xs">
          <!-- Product picker -->
          <div>
            <label class="block text-slate-400 mb-1">Select Product</label>
            <select
              v-model="selectedProductId"
              class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-white"
            >
              <option v-for="p in productStore.products" :key="p.id" :value="p.id">
                {{ p.name }} ({{ p.product_type }})
              </option>
            </select>
          </div>

          <!-- Star rating picker -->
          <div>
            <label class="block text-slate-400 mb-1">Your Rating</label>
            <div class="flex items-center space-x-2 text-2xl text-amber-400 cursor-pointer">
              <span
                v-for="s in 5"
                :key="s"
                @click="formRating = s"
                :class="s <= formRating ? 'text-amber-400' : 'text-slate-700'"
              >
                ★
              </span>
              <span class="text-xs text-slate-400 font-bold ml-2">({{ formRating }} / 5 Stars)</span>
            </div>
          </div>

          <!-- Author info -->
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-slate-400 mb-1">Your Name</label>
              <input
                type="text"
                v-model="formAuthorName"
                placeholder="Marcus Vance"
                class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-white focus:outline-none"
              />
            </div>
            <div>
              <label class="block text-slate-400 mb-1">Email</label>
              <input
                type="email"
                v-model="formAuthorEmail"
                placeholder="marcus@example.com"
                class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-white focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label class="block text-slate-400 mb-1">Review Headline</label>
            <input
              type="text"
              v-model="formTitle"
              placeholder="Game changer for my daily workflow!"
              class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-white focus:outline-none"
            />
          </div>

          <div>
            <label class="block text-slate-400 mb-1">Detailed Feedback</label>
            <textarea
              v-model="formComment"
              rows="3"
              placeholder="Share details about performance, build quality, usability, or learning outcomes..."
              class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-white focus:outline-none"
            ></textarea>
          </div>

          <!-- Photo Upload -->
          <div>
            <label class="block text-slate-400 mb-1">Photo Upload Testimonial (Optional)</label>
            <input
              type="file"
              accept="image/*"
              @change="handlePhotoUpload"
              class="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-slate-300 text-xs file:mr-3 file:py-1 file:px-2 file:rounded-lg file:border-0 file:text-xs file:bg-indigo-600 file:text-white"
            />
            <div v-if="previewImage" class="mt-2 w-24 h-24 rounded-xl overflow-hidden border border-slate-700">
              <img :src="previewImage" alt="Upload Preview" class="w-full h-full object-cover" />
            </div>
          </div>

          <button
            @click="submitReview"
            :disabled="!formAuthorName || !formComment"
            class="w-full py-3 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white font-bold text-xs rounded-xl shadow-lg transition-transform active:scale-95"
          >
            Publish Verified Review 🚀
          </button>
        </div>
      </div>
    </div>

  </div>
</template>
