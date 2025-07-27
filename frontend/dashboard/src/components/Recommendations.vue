<template>
  <div class="recommendations">
    <h2>Energy Saving Recommendations</h2>
    <div v-if="error" class="error">{{ error }}</div>
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
      error: null,
    };
  },
  mounted() {
    this.getLocation();
  },
  methods: {
    getLocation() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(this.getRecommendations, this.handleLocationError);
      } else {
        this.error = "Geolocation is not supported by this browser.";
      }
    },
    getRecommendations(position) {
      const { latitude, longitude } = position.coords;
      axios.get(`/api/recommendations/?latitude=${latitude}&longitude=${longitude}`)
        .then(response => {
          this.recommendations = response.data;
        })
        .catch(error => {
          console.error(error);
          this.error = "Could not get recommendations.";
        });
    },
    handleLocationError(error) {
      switch(error.code) {
        case error.PERMISSION_DENIED:
          this.error = "User denied the request for Geolocation."
          break;
        case error.POSITION_UNAVAILABLE:
          this.error = "Location information is unavailable."
          break;
        case error.TIMEOUT:
          this.error = "The request to get user location timed out."
          break;
        case error.UNKNOWN_ERROR:
          this.error = "An unknown error occurred."
          break;
      }
    },
  },
};
</script>

<style scoped>
.recommendations {
  margin-top: 2rem;
}

.error {
  color: red;
}
</style>
