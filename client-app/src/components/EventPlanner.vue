<template>
  <div class="container">
    <h1>Event Planner</h1>
    <div class="input-container">
      <input v-model="query" placeholder="Enter your query" />
      <button @click="executeQuery">Execute</button>
    </div>
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
    </div>
    <div class="response-container" v-if="!loading && response">
      <template v-if="response.type === 'event_plan'">
        <h2>Event Schedule</h2>
        <div class="summary" v-html="renderedSummary"></div>
        <table>
          <thead>
            <tr>
              <th>Day</th>
              <th>Activities</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(day, index) in response.plan" :key="index">
              <td>{{ day.day }}</td>
              <td>
                <ul v-if="day.activities.length">
                  <li v-for="(activity, index) in day.activities" :key="index">
                    {{ getVenueName(activity.venue_id) }}: {{ activity.time }}, {{ activity.description }}
                  </li>
                </ul>
                <span v-else>No Activities</span>
              </td>
            </tr>
          </tbody>
        </table>
      </template>
      <template v-else-if="response.type === 'venues'">
        <h2>Venue Information</h2>
        <div class="venue-cards">
          <div class="card" v-for="venueId in response.venue_ids" :key="venueId">
            <h3>{{ getVenueName(venueId) }}</h3>
            <p><strong>Type:</strong> {{ getVenueType(venueId) }}</p>
            <p><strong>Capacity:</strong> {{ getVenueCapacity(venueId) }}</p>
            <p><strong>Location:</strong> {{ getVenueLocation(venueId) }}</p>
            <p><strong>Price Range:</strong> {{ getVenuePriceRange(venueId) }}</p>
            <p><strong>Amenities:</strong> {{ getVenueAmenities(venueId) }}</p>
          </div>
        </div>
      </template>
      <template v-else-if="response.type === 'error'">
        <div class="error-message">
          <h2>Error</h2>
          <p>{{ response.message || 'There was an error processing your request. Please try again.' }}</p>
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
      venues: [],
      venueMap: {},
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
      this.response = null;
      try {
        const result = await axios.post('/api/process_query', { query: this.query });
        this.response = result.data;
      } catch (error) {
        console.error(error);
        this.response = { type: 'error', message: error.message };
      } finally {
        this.loading = false;
      }
    },
    async fetchVenues() {
      try {
        const result = await axios.get('/api/venues');
        this.venues = result.data.venues;
        this.venueMap = this.venues.reduce((map, venue) => {
          map[venue.id] = venue;
          return map;
        }, {});
      } catch (error) {
        console.error(error);
      }
    },
    getVenueName(venueId) {
      return this.venueMap[venueId]?.name || 'Unknown Venue';
    },
    getVenueType(venueId) {
      return this.venueMap[venueId]?.type || 'Unknown';
    },
    getVenueCapacity(venueId) {
      return this.venueMap[venueId]?.capacity || 'Unknown';
    },
    getVenueLocation(venueId) {
      return this.venueMap[venueId]?.location || 'Unknown';
    },
    getVenuePriceRange(venueId) {
      return this.venueMap[venueId]?.price_range || 'Unknown';
    },
    getVenueAmenities(venueId) {
      return this.venueMap[venueId]?.amenities?.join(', ') || 'None';
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
    this.fetchVenues();
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
.venue-cards {
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
</style> 