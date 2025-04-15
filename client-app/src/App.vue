<!-- src/App.vue -->
<template>
  <div id="app">
    <EventPlanner />
  </div>
</template>

<script>
import EventPlanner from './components/EventPlanner.vue';

export default {
  name: 'App',
  components: {
    EventPlanner,
  },
};
</script>

<style>
/* Add any global styles you need here */
</style>
