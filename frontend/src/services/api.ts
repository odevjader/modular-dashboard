// frontend/src/services/api.ts

// Read the API base URL from environment variables populated by Vite
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'; // Includes /api prefix now

// --- Type Definitions ---

// System Info Module
export interface SystemInfoResponse {
    environment: string;
    project_name: string;
    server_time_utc: string; // Datetime comes as string in JSON
    api_prefix: string;
}

// AI Test Module - ADDED TYPES
export interface AITestInput {
    text: string;
}

export interface AITestResponse {
    response: string;
}


// --- Generic API Client (Should remain unchanged) ---
async function apiClient<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`; // API_BASE_URL already includes /api

    const defaultHeaders: HeadersInit = {
        'Content-Type': 'application/json',
    };

    const config: RequestInit = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers,
        },
    };

    // Basic console log for debugging outgoing requests
    // console.log(`API Request: ${config.method || 'GET'} ${url}`);

    try {
        const response = await fetch(url, config);

        if (!response.ok) {
            let errorData;
            try {
                errorData = await response.json();
            } catch (e) { /* Ignore */ }
            throw new Error(
                `API request failed: ${response.status} ${response.statusText}${errorData ? ` - ${JSON.stringify(errorData)}` : ''}`
            );
        }

        if (response.status === 204) {
            return {} as T;
        }
        return await response.json() as T;

    } catch (error) {
        console.error('API Client Error:', error);
        throw error;
    }
}

// --- Specific API Functions ---

/** Fetches system status information from the backend. */
export const getSystemInfo = (): Promise<SystemInfoResponse> => {
    return apiClient<SystemInfoResponse>('/info/v1/status');
};

/** Sends a text prompt to the AI Test backend endpoint. */
export const postAITestPing = (payload: AITestInput): Promise<AITestResponse> => {
    return apiClient<AITestResponse>('/ai_test/v1/ping', {
        method: 'POST',
        body: JSON.stringify(payload), // Send payload as JSON string
    });
};

// Add other specific API functions here later...