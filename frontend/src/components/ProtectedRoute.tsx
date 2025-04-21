import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';

export const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const { token } = useAuthStore();
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
};
