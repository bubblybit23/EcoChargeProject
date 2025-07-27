<template>
  <div class="recommendations">
    <h2>Energy Saving Recommendations</h2>
    <ul>
      <li v-for="recommendation in recommendations" :key="recommendation">
        {{ recommendation }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Recommendations',
  data() {
    return {
      recommendations: [],
    };
  },
  mounted() {
    this.getRecommendations();
  },
  methods: {
    getRecommendations() {
      axios.get('/api/recommendations/')
        .then(response => {
          this.recommendations = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
  },
};
</script>

<style scoped>
.recommendations {
  margin-top: 2rem;
}
</style>
