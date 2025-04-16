// frontend/src/services/api.ts

// Read the API base URL from environment variables populated by Vite
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'; // Fallback if not set

// --- Type Definition for System Info Response ---
// TODO: Consider moving shared types to a dedicated types directory or package later
export interface SystemInfoResponse {
    environment: string;
    project_name: string;
    server_time_utc: string; // Datetime comes as string in JSON
    api_prefix: string;
}

// --- Generic API Client ---
/**
 * Makes a request to the backend API.
 * @param endpoint The API endpoint path (e.g., '/health/v1/health'). Should start with '/'.
 * @param options Optional fetch options (method, headers, body, etc.). Defaults to GET.
 * @returns A promise that resolves with the JSON response.
 * @throws An error if the network response is not ok.
 */
async function apiClient<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;

    const defaultHeaders: HeadersInit = {
        'Content-Type': 'application/json',
        // 'Authorization': `Bearer ${getToken()}` // Add later for auth
    };

    const config: RequestInit = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers,
        },
    };

    try {
        const response = await fetch(url, config);

        if (!response.ok) {
            let errorData;
            try {
                errorData = await response.json();
            } catch (e) { /* Ignore if response body is not JSON */ }
            throw new Error(
                `API request failed: ${response.status} ${response.statusText}${errorData ? ` - ${JSON.stringify(errorData)}` : ''}`
            );
        }

        if (response.status === 204) { // No Content
            return {} as T;
        }
        return await response.json() as T;

    } catch (error) {
        console.error('API Client Error:', error);
        throw error; // Re-throw to be handled by caller
    }
}

// --- Specific API Functions ---

/**
 * Fetches system status information from the backend.
 */
export const getSystemInfo = (): Promise<SystemInfoResponse> => {
    // Endpoint path matches the backend route registration
    return apiClient<SystemInfoResponse>('/info/v1/status');
};

// Example health check function (can add if needed)
// export const getHealth = (): Promise<{ status: string; message: string }> => {
//     return apiClient<{ status: string; message: string }>('/health/v1/health');
// };


// Export the generic client if needed elsewhere, though specific functions are preferred
// export default apiClient;