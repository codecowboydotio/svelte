<!-- App.svelte -->
<script>
  import { onMount } from 'svelte';
  
  // State for storing people data and loading state
  let people = [];
  let isLoading = true;
  let error = null;
  
  // Function to fetch data from the API
  async function fetchPeople() {
    isLoading = true;
    try {
      const response = await fetch('https://jsonplaceholder.typicode.com/users');
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      people = await response.json();
      error = null;
    } catch (err) {
      console.error('Failed to fetch people:', err);
      error = err.message;
      people = [];
    } finally {
      isLoading = false;
    }
  }
  
  // Fetch data when component mounts
  onMount(fetchPeople);
</script>

<main>
  <h1>People Directory</h1>
  
  {#if isLoading}
    <div class="loading">Loading people data...</div>
  {:else if error}
    <div class="error">
      <p>Error loading people: {error}</p>
      <button on:click={fetchPeople}>Try Again</button>
    </div>
  {:else if people.length === 0}
    <div class="empty">No people found.</div>
  {:else}
    <div class="people-list">
      {#each people as person (person.id)}
        <div class="person-card">
          <h2>{person.name}</h2>
          {#if person.email}
            <p>Email: {person.email}</p>
          {/if}
          {#if person.phone}
            <p>Phone: {person.phone}</p>
          {/if}
          {#if person.location}
            <p>Location: {person.location}</p>
          {/if}
          <!-- Add more fields as needed -->
        </div>
      {/each}
    </div>
  {/if}
  
  <div class="controls">
    <button on:click={fetchPeople} disabled={isLoading}>
      {isLoading ? 'Loading...' : 'Refresh Data'}
    </button>
  </div>
</main>

<style>
  main {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  
  h1 {
    color: #333;
    text-align: center;
    margin-bottom: 30px;
  }
  
  .loading, .error, .empty {
    text-align: center;
    padding: 20px;
    margin: 20px 0;
    border-radius: 4px;
  }
  
  .loading {
    background-color: #f8f9fa;
    color: #6c757d;
  }
  
  .error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
  }
  
  .empty {
    background-color: #e2e3e5;
    color: #383d41;
  }
  
  .people-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 20px;
  }
  
  .person-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
  }
  
  .person-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.15);
  }
  
  .person-card h2 {
    margin-top: 0;
    color: #0066cc;
    font-size: 1.2rem;
  }
  
  .controls {
    text-align: center;
    margin-top: 20px;
  }
  
  button {
    background-color: #0066cc;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s ease;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
</style>
