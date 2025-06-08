import React, { Suspense } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import { Login } from './components/Login';
import { ProtectedRoute } from './components/ProtectedRoute';
import AdminUsers from './components/AdminUsers';
import HomePage from './pages/HomePage'; // Make sure HomePage is imported
import { getModuleRegistry, ModuleConfig } from './config/moduleRegistry'; // Ensure correct path
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';

function App() {
  const moduleRegistry = getModuleRegistry();

  return (
    <Router>
      <Suspense fallback={
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
          <CircularProgress />
        </Box>
      }>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <MainLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<HomePage />} />
            <Route path="/admin/users" element={<ProtectedRoute roles={['admin']}><AdminUsers /></ProtectedRoute>} />
            {/* Dynamic module routes */}
            {Object.values(moduleRegistry).map((module: ModuleConfig) =>
              module.routes.map((route) => (
                <Route
                  key={`${module.basePath}${route.path}`}
                  path={`${module.basePath}${route.path === '/' ? '' : route.path}`} // Handle base path and nested root
                  element={
                    <ProtectedRoute adminOnly={module.adminOnly}>
                      <route.component />
                    </ProtectedRoute>
                  }
                />
              ))
            )}
          </Route>
        </Routes>
      </Suspense>
    </Router>
  );
}

export default App;
