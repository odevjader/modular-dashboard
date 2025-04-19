// frontend/src/services/api.ts

// Read the API base URL from environment variables populated by Vite
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'; // Includes /api prefix now

// --- Type Definitions ---

// System Info Module
export interface SystemInfoResponse {
    environment: string;
    project_name: string;
    server_time_utc: string;
    api_prefix: string;
}

// AI Test Module
export interface AITestInput {
    text: string;
}
export interface AITestResponse {
    response: string;
}

// Gerador Quesitos Module - ADDED TYPES
export interface RespostaQuesitos {
    quesitos_texto: string;
}


// --- Generic API Client (for JSON endpoints) ---
async function apiClient<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;

    const defaultHeaders: HeadersInit = {
        'Content-Type': 'application/json',
        // Add other default headers like Authorization if needed later
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
            try { errorData = await response.json(); } catch (e) { /* Ignore */ }
            throw new Error(`API request failed: ${response.status} ${response.statusText}${errorData ? ` - ${JSON.stringify(errorData)}` : ''}`);
        }
        if (response.status === 204) { return {} as T; }
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
        body: JSON.stringify(payload),
    });
};

/** Uploads PDF and inputs to generate quesitos. Uses FormData. */
export const postGerarQuesitos = async (formData: FormData): Promise<RespostaQuesitos> => {
    const url = `${API_BASE_URL}/gerador_quesitos/v1/gerar`; // Construct full URL

    try {
        // When using FormData, DO NOT set Content-Type header manually.
        // The browser will set it correctly with the boundary.
        const response = await fetch(url, {
            method: 'POST',
            body: formData,
            // No 'Content-Type': 'multipart/form-data' header here!
        });

        if (!response.ok) {
            let errorData;
            try { errorData = await response.json(); } catch (e) { /* Ignore */ }
            throw new Error(`API request failed: ${response.status} ${response.statusText}${errorData ? ` - ${JSON.stringify(errorData)}` : ''}`);
        }

        // Assuming the response is JSON even though request was FormData
        return await response.json() as RespostaQuesitos;

    } catch (error) {
        console.error('Error in postGerarQuesitos:', error);
        throw error; // Re-throw error for the component to handle
    }
};


// Add other specific API functions here later...