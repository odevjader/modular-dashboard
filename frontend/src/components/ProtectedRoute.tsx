// frontend/src/components/ProtectedRoute.tsx
import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore'; // Assuming authStore provides user role info
import { ReactNode } from 'react'; // Import ReactNode for children type

// Define the props for ProtectedRoute
interface ProtectedRouteProps {
  children: ReactNode;
  roles?: string | string[]; // Optional: roles required to access the route
}

export const ProtectedRoute = ({ children, roles }: ProtectedRouteProps) => {
  // Get authentication status and user information from the store
  // Assuming useAuthStore() returns an object that includes:
  // - `token` (or a boolean like `isAuthenticated`)
  // - `user` (an object which might contain a `role` or `roles` property)
  const { token, user } = useAuthStore(state => ({ token: state.token, user: state.user }));

  // 1. Check for basic authentication
  if (!token) {
    // Not authenticated, redirect to login
    return <Navigate to="/login" replace />;
  }

  // 2. Check for role-based authorization if 'roles' prop is provided
  if (roles) {
    const userRoles = user?.roles || (user?.role ? [user.role] : []); // Adapt based on how roles are stored in `user` object
                                                                    // Handles user.roles (array) or user.role (single string)

    const requiredRoles = Array.isArray(roles) ? roles : [roles]; // Ensure requiredRoles is an array

    // Check if the user has at least one of the required roles
    const hasRequiredRole = requiredRoles.some(role => userRoles.includes(role));

    if (!hasRequiredRole) {
      // User is authenticated but does not have the required role(s)
      // Redirect to an unauthorized page or home. For now, redirecting to home ('/')
      // A dedicated '/unauthorized' page would be better in a full app.
      // If no specific "home" is safe, login might be an option, or a generic dashboard.
      // For this example, let's assume redirecting to "/" is a safe fallback.
      // If "/" itself requires a role they don't have, this could loop if not handled carefully.
      // Best practice: have a specific unauthorized page, or a default page all authenticated users can see.
      alert("You do not have permission to access this page."); // Simple feedback
      return <Navigate to="/" replace />; // Redirect to a safe default page
    }
  }

  // If authenticated and (no specific roles required OR user has required roles), render the children
  return <>{children}</>;
};

// Note on useAuthStore:
// The authStore (e.g., Zustand or Redux store) needs to be structured to provide:
// 1. A token or boolean for authentication status.
// 2. A user object that contains role information (e.g., user.role as a string or user.roles as an array of strings).
// Example of what useAuthStore might look like (Zustand):
/*
import create from 'zustand';

interface User {
  id: string;
  username: string;
  role: string; // or roles: string[];
  // other user properties
}

interface AuthState {
  token: string | null;
  user: User | null;
  login: (token: string, user: User) => void;
  logout: () => void;
  // ... other actions and state properties
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('authToken'), // Initialize from localStorage
  user: JSON.parse(localStorage.getItem('authUser') || 'null'), // Initialize from localStorage
  login: (token, user) => {
    localStorage.setItem('authToken', token);
    localStorage.setItem('authUser', JSON.stringify(user));
    set({ token, user });
  },
  logout: () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('authUser');
    set({ token: null, user: null });
  },
  // Ensure your store provides the user object with a role or roles field.
}));
*/
