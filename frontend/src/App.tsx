// frontend/src/App.tsx
import { Suspense } from 'react'; // Needed for React.lazy
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import { Login } from './components/Login';
import { ProtectedRoute } from './components/ProtectedRoute'; // Assuming ProtectedRoute handles role checks or can be adapted
import { APP_MODULES } from './config/moduleRegistry'; // Import the module definitions

// A simple loading fallback for lazy loaded components
const LoadingFallback = () => <div>Loading page...</div>; // Or a more sophisticated spinner

function App() {
  return (
    <Router>
      <Suspense fallback={<LoadingFallback />}> {/* Suspense wrapper for all lazy loaded routes */}
        <Routes>
          {/* Public Route for Login */}
          <Route path="/login" element={<Login />} />

          {/* Routes that use MainLayout */}
          {/* Option 1: Single ProtectedRoute wrapping MainLayout, role checks per module happen inside MainLayout or module component.
              Option 2: Wrap each dynamic route with ProtectedRoute if it has a requiredRole. (More granular)
              Let's go with Option 2 for more explicit route protection based on module config.
          */}

          {/* Static protected routes that might not be in APP_MODULES or need special handling (if any) */}
          {/* For example, a root redirect IF no HomePage module is defined for "/" */}
          {/* <Route path="/" element={<ProtectedRoute><MainLayout><Navigate to="/some-default-path" /></MainLayout></ProtectedRoute>} /> */}


          {/* Dynamically generate routes from APP_MODULES */}
          {APP_MODULES.map((module) => {
            const PageComponent = module.component; // Lazy loaded component

            // If the module requires a specific role, wrap its route with ProtectedRoute.
            // ProtectedRoute itself might need access to user's roles from a store (e.g., authStore).
            // The `role` prop for ProtectedRoute would be `module.requiredRole`.
            if (module.requiredRole) {
              return (
                <Route
                  key={module.id}
                  path={module.path}
                  element={
                    <ProtectedRoute roles={module.requiredRole}> {/* Pass required roles to ProtectedRoute */}
                      <MainLayout>
                        <PageComponent />
                      </MainLayout>
                    </ProtectedRoute>
                  }
                />
              );
            } else {
              // Module does not require a specific role, but still needs to be within a protected context (MainLayout)
              // Assuming MainLayout itself is within a general ProtectedRoute or handles auth checks.
              // For simplicity, let's assume a general ProtectedRoute wraps MainLayout for non-role-specific routes.
              // Re-evaluating: The plan was "ProtectedRoute still wraps these dynamic routes".
              // So, all routes within MainLayout should be protected.
              return (
                <Route
                  key={module.id}
                  path={module.path}
                  element={
                    <ProtectedRoute> {/* General protection for authenticated users */}
                      <MainLayout>
                        <PageComponent />
                      </MainLayout>
                    </ProtectedRoute>
                  }
                />
              );
            }
          })}

          {/* Fallback for any unmatched routes - redirect to login or a 404 page */}
          {/* If a default route like "/" is in APP_MODULES, this might not be hit often for logged-in users. */}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Suspense>
    </Router>
  );
}

export default App;

/*
NOTES on ProtectedRoute:
The existing `ProtectedRoute.tsx` probably looks something like this:

const ProtectedRoute = ({ children, roles }) => {
  const { isAuthenticated, user } = useAuthStore(); // Or however auth state is accessed

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (roles) { // If roles are specified for this route
    const userRoles = Array.isArray(user?.role) ? user.role : [user?.role];
    const requiredRoles = Array.isArray(roles) ? roles : [roles];
    if (!requiredRoles.some(role => userRoles.includes(role))) {
      // User does not have the required role
      return <Navigate to="/unauthorized" replace />; // Or to a "not authorized" page
    }
  }

  return children;
};

This subtask assumes ProtectedRoute can accept a `roles` prop (string or array of strings)
and will handle the role-based access control. If it doesn't, ProtectedRoute would need
to be updated accordingly in a separate step (or this step if minor).
The `module.requiredRole` from `moduleRegistry` will be passed as the `roles` prop.
*/
