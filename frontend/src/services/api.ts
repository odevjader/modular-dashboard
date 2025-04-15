// frontend/src/services/api.ts

// Read the API base URL from environment variables populated by Vite
// VITE_ prefix is necessary for Vite to expose it to the client-side code.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'; // Fallback to relative /api if not set

console.log(`API Base URL: ${API_BASE_URL}`); // Log for debugging during development

/**
 * Makes a request to the backend API.
 * @param endpoint The API endpoint path (e.g., '/health/v1/health'). Should start with '/'.
 * @param options Optional fetch options (method, headers, body, etc.). Defaults to GET.
 * @returns A promise that resolves with the JSON response.
 * @throws An error if the network response is not ok.
 */
async function apiClient<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`; // Construct the full URL

  // Default headers (can be extended or overridden by options)
  const defaultHeaders: HeadersInit = {
    'Content-Type': 'application/json',
    // Add other default headers like Authorization later if needed
    // 'Authorization': `Bearer ${getToken()}`
  };

  const config: RequestInit = {
    ...options, // Spread incoming options
    headers: {
      ...defaultHeaders, // Apply defaults
      ...options.headers, // Apply specific headers from options, potentially overriding defaults
    },
  };

  try {
    const response = await fetch(url, config);

    if (!response.ok) {
      // Attempt to parse error details from response body
      let errorData;
      try {
        errorData = await response.json();
      } catch (e) {
        // Ignore if response body is not JSON
      }
      // Throw an error with status text and potentially more details
      throw new Error(
        `API request failed: ${response.status} ${response.statusText}${errorData ? ` - ${JSON.stringify(errorData)}` : ''}`
      );
    }

    // Handle cases where response might be empty (e.g., 204 No Content)
    if (response.status === 204) {
      return {} as T; // Or return null, depending on expected behavior
    }

    // Assume response is JSON for other successful requests
    return await response.json() as T;

  } catch (error) {
    console.error('API Client Error:', error);
    // Re-throw the error to be caught by the calling function
    throw error;
  }
}

// Example specific API functions (optional, can be added as needed)
// export const getHealth = () => {
//   // Note: Endpoint should match the path defined in FastAPI router inclusion
//   return apiClient<{ status: string; message: string }>('/health/v1/health');
// };

export default apiClient;