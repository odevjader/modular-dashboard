// frontend/src/services/api.ts

// Read the API base URL from environment variables populated by Vite
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

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

// Gerador Quesitos Module
export interface RespostaQuesitos {
    quesitos_texto: string;
}

// Auth Module
export interface LoginResponse {
    access_token: string;
    token_type: string;
}
export interface UserResponse {
    id: number;
    email: string;
    role: string;
}

// --- Generic API Client (for JSON endpoints) ---
async function apiClient<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    const token = localStorage.getItem('token');

    const defaultHeaders: HeadersInit = {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
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
    const url = `${API_BASE_URL}/gerador_quesitos/v1/gerar`;
    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData,
        });
        if (!response.ok) {
            let errorData;
            try { errorData = await response.json(); } catch (e) { /* Ignore */ }
            throw new Error(`API request failed: ${response.status} ${response.statusText}${errorData ? ` - ${JSON.stringify(errorData)}` : ''}`);
        }
        return await response.json() as RespostaQuesitos;
    } catch (error) {
        console.error('Error in postGerarQuesitos:', error);
        throw error;
    }
};

/** Logs in a user and returns a JWT token. */
export const login = async (email: string, password: string): Promise<LoginResponse> => {
    const url = `${API_BASE_URL}/auth/v1/login`;
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({
                username: email,
                password,
                grant_type: 'password',
                client_id: 'string',
                client_secret: 'string',
            }),
        });
        if (!response.ok) {
            let errorData;
            try { errorData = await response.json(); } catch (e) { /* Ignore */ }
            throw new Error(`Login failed: ${response.status} ${response.statusText}${errorData ? ` - ${JSON.stringify(errorData)}` : ''}`);
        }
        return await response.json() as LoginResponse;
    } catch (error) {
        console.error('Error in login:', error);
        throw error;
    }
};

/** Fetches the current user's information. */
export const getCurrentUser = async (token: string): Promise<UserResponse> => {
    return apiClient<UserResponse>('/auth/v1/users/me', {
        headers: { Authorization: `Bearer ${token}` },
    });
};