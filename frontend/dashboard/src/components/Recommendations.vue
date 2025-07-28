<template>
  <div class="recommendations">
    <h2>Energy Saving Recommendations</h2>
    <div v-if="error" class="error">
      <p>{{ getErrorMessage(error) }}</p>
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
      }, {
        headers: {
          'X-Client-Region': Intl.DateTimeFormat().resolvedOptions().timeZone,
        }
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
          this.error = error;
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
    getErrorMessage(error) {
      if (error?.response?.data?.error?.includes('EMISSIONS_DATA')) {
        return "Energy data service is currently unavailable";
      }
      return "Could not get recommendations";
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
