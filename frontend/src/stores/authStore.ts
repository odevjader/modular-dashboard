import { create } from 'zustand';
import { login, getCurrentUser } from '../services/api';

interface User {
  id: number;
  email: string;
  role: string;
}

interface AuthState {
  token: string | null;
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('token'),
  user: null,
  login: async (email: string, password: string) => {
    try {
      const { access_token } = await login(email, password);
      localStorage.setItem('token', access_token);
      const user = await getCurrentUser(access_token);
      set({ token: access_token, user });
    } catch (error) {
      throw new Error('Login failed');
    }
  },
  logout: () => {
    localStorage.removeItem('token');
    set({ token: null, user: null });
  },
}));
