// frontend/src/components/ProtectedRoute.tsx
import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore'; // Assuming authStore provides user role info
import { ReactNode } from 'react'; // Import ReactNode for children type

// Define the props for ProtectedRoute
interface ProtectedRouteProps {
  children: ReactNode;
  roles?: string | string[]; // Optional: roles required to access the route
  adminOnly?: boolean; // Add this
}

export const ProtectedRoute = ({ children, roles, adminOnly }: ProtectedRouteProps) => {
  const token = useAuthStore(state => state.token);
  const user = useAuthStore(state => state.user);

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  let effectiveRoles = roles;
  if (adminOnly && !effectiveRoles) {
    effectiveRoles = ['admin']; // Convert adminOnly to a role requirement
  }

  if (effectiveRoles) {
    if (!user || !user.role) { // If roles are required, user and user.role must exist
      // This handles cases where user data might not be loaded yet or role is missing.
      // Consider a loading indicator or specific handling if user loading is async on refresh.
      // For now, redirecting to login if user/role is missing for a role-protected route.
      // console.warn("ProtectedRoute: User data or role not available for role check. Redirecting to login.");
      return <Navigate to="/login" replace />;
    }

    const userRoleString = user.role.toLowerCase(); // Ensure user's role is lowercased
    const userRolesArray = [userRoleString]; // Assuming user.role is a single string like "admin" or "user"

    const requiredRoles = Array.isArray(effectiveRoles)
                          ? effectiveRoles.map(r => r.toLowerCase())
                          : [effectiveRoles.toLowerCase()];

    const hasRequiredRole = requiredRoles.some(role => userRolesArray.includes(role));

    if (!hasRequiredRole) {
      // console.warn(`ProtectedRoute: Role check failed. User roles: ${userRolesArray.join(', ')}, Required roles: ${requiredRoles.join(', ')}`);
      alert("You do not have permission to access this page.");
      return <Navigate to="/" replace />;
    }
  }
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
