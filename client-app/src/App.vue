<!-- src/App.vue -->
<template>
  <div id="app">
    <WorkoutPlanner />
  </div>
</template>

<script>
import WorkoutPlanner from './components/WorkoutPlanner.vue';

export default {
  name: 'App',
  components: {
    WorkoutPlanner,
  },
};
</script>

<style>
/* Add any global styles you need here */
</style>
