<template>
  <div class="recommendations">
    <h2>Energy Saving Recommendations</h2>
    <div v-if="error" class="error">
      <p>{{ error }}</p>
      <p>Please ensure that you have enabled location services in your browser and that you have a stable internet connection.</p>
      <p>If you continue to experience issues, please try again later.</p>
    </div>
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
      axios.post('/api/recommendations/', {
        lat: latitude,
        lng: longitude,
      })
        .then(response => {
          if (response.data.error) {
            this.error = response.data.error;
          } else {
            this.recommendations = response.data;
          }
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
  border: 1px solid red;
  padding: 1rem;
  margin-bottom: 1rem;
}
</style>
