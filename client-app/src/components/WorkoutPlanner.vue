<template>
  <div class="container">
    <h1>Workout Planner</h1>
    <div class="input-container">
      <input v-model="query" placeholder="Enter your query" />
      <button @click="executeQuery">Execute</button>
    </div>
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
    </div>
    <div class="response-container" v-if="!loading && response">
      <template v-if="response.type === 'workout_plan'">
        <h2>7-Day Workout Plan</h2>
        <div class="summary" v-html="renderedSummary"></div>
        <table>
          <thead>
            <tr>
              <th>Day</th>
              <th>Exercises</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(day, index) in response.plan" :key="index">
              <td>{{ day.day }}</td>
              <td>
                <ul v-if="day.exercises.length">
                  <li v-for="(exercise, index) in day.exercises" :key="index">
                    {{ getExerciseName(exercise.exercise_id) }}: {{ exercise.sets }} sets, {{ exercise.repetitions }}
                  </li>
                </ul>
                <span v-else>Rest Day</span>
              </td>
            </tr>
          </tbody>
        </table>
      </template>
      <template v-else-if="response.type === 'exercises'">
        <h2>Exercise Information</h2>
        <div class="exercise-cards">
          <div class="card" v-for="exerciseId in response.exercise_ids" :key="exerciseId">
            <h3>{{ getExerciseName(exerciseId) }}</h3>
            <p>{{ getExerciseDescription(exerciseId) }}</p>
            <p><strong>Level:</strong> {{ getExerciseLevel(exerciseId) }}</p>
            <p><strong>Muscle Groups:</strong> {{ getExerciseMuscleGroups(exerciseId).join(', ') }}</p>
            <p><strong>Requirements:</strong> {{ getExerciseRequirements(exerciseId) }}</p>
            <p><strong>Home Friendly:</strong> {{ getExerciseHomeFriendly(exerciseId) ? 'Yes' : 'No' }}</p>
          </div>
        </div>
      </template>
      <template v-else-if="response.type === 'error'">
        <div class="error-message">
          <h2>Error</h2>
          <p>There was an error processing your request. Please try again.</p>
        </div>
      </template>
      <template v-else-if="response.type === 'not_supported'">
        <h2>Request Not Supported</h2>
        <p>Sorry, your request is not supported.</p>
      </template>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { marked } from 'marked';

export default {
  data() {
    return {
      query: '',
      response: null,
      loading: false,
      exercises: [],
      exerciseMap: {},
    };
  },
  computed: {
    renderedSummary() {
      return this.response && this.response.summary ? marked(this.response.summary) : '';
    },
  },
  methods: {
    async executeQuery() {
      this.loading = true;
      this.response = null; // Clear previous response
      try {
        const result = await axios.post('/api/process_query', { query: this.query });
        this.response = result.data;
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    async fetchExercises() {
      try {
        const result = await axios.get('/api/exercises');
        this.exercises = result.data.exercises;
        this.exerciseMap = this.exercises.reduce((map, exercise) => {
          map[exercise.id] = exercise;
          return map;
        }, {});
      } catch (error) {
        console.error(error);
      }
    },
    getExerciseName(exerciseId) {
      return this.exerciseMap[exerciseId]?.name || 'Unknown Exercise';
    },
    getExerciseDescription(exerciseId) {
      return this.exerciseMap[exerciseId]?.description || 'No description available';
    },
    getExerciseLevel(exerciseId) {
      return this.exerciseMap[exerciseId]?.level || 'Unknown';
    },
    getExerciseMuscleGroups(exerciseId) {
      return this.exerciseMap[exerciseId]?.muscle_groups || [];
    },
    getExerciseRequirements(exerciseId) {
      return this.exerciseMap[exerciseId]?.requirements || 'Unknown';
    },
    getExerciseHomeFriendly(exerciseId) {
      return this.exerciseMap[exerciseId]?.home_friendly || false;
    },
    checkUrlForQuery() {
      const urlParams = new URLSearchParams(window.location.search);
      const urlQuery = urlParams.get('query');
      if (urlQuery) {
        this.query = urlQuery;
        this.executeQuery();
      }
    },
  },
  mounted() {
    this.fetchExercises();
    this.checkUrlForQuery();
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
h1 {
  text-align: center;
  color: #333;
}
.input-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
input {
  flex: 1;
  padding: 10px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}
button:hover {
  background-color: #0056b3;
}
.response-container {
  margin-top: 20px;
}
.summary {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #e9f7ff;
  border-left: 4px solid #007bff;
  border-radius: 4px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
th, td {
  padding: 10px;
  text-align: left;
  border: 1px solid #ddd;
}
th {
  background-color: #f4f4f4;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  margin-bottom: 5px;
}
.exercise-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
.card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: calc(33% - 20px);
}
.card h3 {
  margin-top: 0;
}

.loading {
  text-align: center;
  font-size: 1.5em;
  color: #007bff;
}
.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top: 4px solid #007bff;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 20px auto;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.error-message {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  padding: 20px;
  border-radius: 4px;
  margin-top: 20px;
}
.error-message h2 {
  margin: 0 0 10px 0;
}
</style>
