<template>
    <div>
      <h1>Arbitrage Data</h1>
      <ul>
        <li v-for="dataItem in arbitrageData" :key="dataItem.id">
          <!-- Adjust the property names based on your API response structure -->
          {{ dataItem }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        arbitrageData: [],
      };
    },
    mounted() {
      this.fetchArbitrageData();
    },
    methods: {
      async fetchArbitrageData() {
        try {
          const response = await axios.get('http://127.0.0.1:8000/ArbBackend/arbitrage/169');
          this.arbitrageData = response.data;
        } catch (error) {
          console.error('Error fetching arbitrage data:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add your component-specific styles here */
  </style>
  