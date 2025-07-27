<template>
  <DashboardLayout>
    <Recommendations />
  </DashboardLayout>
</template>

<script>
import DashboardLayout from './layouts/DashboardLayout.vue';
import Recommendations from './components/Recommendations.vue';

export default {
  name: 'App',
  components: {
    DashboardLayout,
    Recommendations,
  },
};
</script>
