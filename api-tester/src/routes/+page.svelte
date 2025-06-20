<!-- src/routes/+page.svelte -->
<script>
  import { browser } from '$app/environment';
  import { onMount } from 'svelte';

  let url = '';
  let requestData = '{\n  "key": "value"\n}';
  let response = '';
  let loading = false;
  let error = null;
  let showResult = false;
  let method = 'POST'; // Default method selection

  async function handleSubmit() {
    if (!browser) return;
    
    loading = true;
    error = null;
    showResult = true;

    try {
      // Validate URL
      if (!url) throw new Error('URL is required');

      // For POST requests, validate JSON
      let parsedData;
      if (method === 'POST') {
        try {
          parsedData = JSON.parse(requestData);
        } catch (e) {
          throw new Error(`Invalid JSON: ${e.message}`);
        }
      }

      // Configure fetch options based on the selected method
      const fetchOptions = {
        method: method,
        headers: {
          'Content-Type': 'application/json'
        }
      };

      // Only include body for POST requests
      if (method === 'POST') {
        fetchOptions.body = requestData;
      }

      const fetchResponse = await fetch(url, fetchOptions);

      const contentType = fetchResponse.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        const jsonResponse = await fetchResponse.json();
        return JSON.stringify(jsonResponse, null, 2);
      } else {
        const textResponse = await fetchResponse.text();
        return textResponse;
      }
    } catch (err) {
      error = err.message;
      return `Error: ${err.message}`;
    } finally {
      loading = false;
    }
  }

  async function makeRequest() {
    response = await handleSubmit();
  }

  function formatJson() {
    try {
      const parsed = JSON.parse(requestData);
      requestData = JSON.stringify(parsed, null, 2);
    } catch (e) {
      // Ignore formatting if JSON is invalid
    }
  }

  function closeResult() {
    showResult = false;
  }
</script>

<svelte:head>
  <title>API Client - SvelteKit</title>
  <meta name="description" content="Simple API client for testing REST endpoints" />
</svelte:head>

<main>
  <div class="container">
    <div class="input-section">
      <h1>API Client</h1>

      <form on:submit|preventDefault={makeRequest}>
        <div class="form-group">
          <label for="url">API Endpoint URL</label>
          <input
            type="text"
            id="url"
            bind:value={url}
            placeholder="https://api.example.com/endpoint"
            required
          />
        </div>

        <div class="form-group">
          <label for="method">Request Method</label>
          <select id="method" bind:value={method}>
            <option value="GET">GET</option>
            <option value="POST">POST</option>
          </select>
        </div>

        {#if method === 'POST'}
          <div class="form-group">
            <label for="data">
              Request Body (JSON)
              <button type="button" class="format-btn" on:click={formatJson}>Format</button>
            </label>
            <textarea
              id="data"
              bind:value={requestData}
              placeholder='"key": "value"'
              rows="10"
              required
            ></textarea>
          </div>
        {/if}

        <button type="submit" class="submit-btn" disabled={loading}>
          {loading ? 'Sending Request...' : `Send ${method} Request`}
        </button>
      </form>
    </div>

  {#if showResult}
    <div class="popup-overlay" on:click={closeResult}>
      <div class="popup-window" on:click|stopPropagation>
        <div class="popup-header">
          <h2>API Response</h2>
          <button class="close-btn" on:click={closeResult}>×</button>
        </div>

        <div class="popup-content">
          {#if loading}
            <div class="loading">
              <div class="spinner"></div>
              <p>Sending request...</p>
            </div>
          {:else if error}
            <div class="error">
              <p>{error}</p>
            </div>
          {:else}
            <pre>{response}</pre>
          {/if}
        </div>
      </div>
    </div>
  {/if}
  </div>
</main>

<style>
  :global(body) {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
      Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f7f9fc;
    color: #333;
  }

  .container {
    min-height: 100vh;
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
  }

  .input-section {
    width: 100%;
  }

  h1 {
    color: #2d3748;
    margin-bottom: 1.5rem;
  }

  .form-group {
    margin-bottom: 1.5rem;
  }

  label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #4a5568;
  }

  input, textarea, select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e2e8f0;
    border-radius: 0.25rem;
    font-size: 1rem;
    font-family: inherit;
    box-sizing: border-box;
  }

  select {
    background-color: white;
    cursor: pointer;
  }

  textarea {
    font-family: monospace;
    resize: vertical;
  }

  .format-btn {
    background: none;
    border: none;
    color: #4299e1;
    cursor: pointer;
    font-size: 0.875rem;
    padding: 0.25rem 0.5rem;
  }

  .format-btn:hover {
    text-decoration: underline;
  }

  .submit-btn {
    background-color: #4299e1;
    color: white;
    border: none;
    border-radius: 0.25rem;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .submit-btn:hover {
    background-color: #3182ce;
  }

  .submit-btn:disabled {
    background-color: #a0aec0;
    cursor: not-allowed;
  }

  .popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    animation: fadeIn 0.2s ease-out;
  }

  .popup-window {
    background-color: white;
    border-radius: 0.5rem;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    max-width: 90vw;
    max-height: 80vh;
    width: 700px;
    display: flex;
    flex-direction: column;
    animation: slideIn 0.3s ease-out;
  }

  .popup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 2rem;
    border-bottom: 1px solid #e2e8f0;
    border-radius: 0.5rem 0.5rem 0 0;
  }

  .popup-header h2 {
    margin: 0;
    color: #2d3748;
  }

  .popup-content {
    padding: 2rem;
    overflow-y: auto;
    flex: 1;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: scale(0.9) translateY(-10px);
    }
    to {
      opacity: 1;
      transform: scale(1) translateY(0);
    }
  }

  pre {
    white-space: pre-wrap;
    word-wrap: break-word;
    background-color: #f9fafb;
    border: 1px solid #e2e8f0;
    border-radius: 0.25rem;
    padding: 1rem;
    overflow-x: auto;
    margin: 0;
    font-family: monospace;
  }

  .loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
  }

  .spinner {
    border: 3px solid #e2e8f0;
    border-top: 3px solid #4299e1;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .error {
    color: #e53e3e;
    border-left: 4px solid #e53e3e;
    padding-left: 1rem;
  }

  @media (max-width: 768px) {
    .container {
      padding: 1rem;
    }

    .popup-window {
      width: 95vw;
      max-height: 90vh;
      margin: 1rem;
    }

    .popup-header {
      padding: 1rem 1.5rem;
    }

    .popup-content {
      padding: 1.5rem;
    }
  }
</style>
