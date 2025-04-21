// frontend/src/App.tsx
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import HomePage from './pages/HomePage';
import SystemInfoPage from './pages/SystemInfoPage';
import AITestPage from './pages/AITestPage';
import PaginaGeradorQuesitos from './pages/PaginaGeradorQuesitos';
import MainLayout from './layouts/MainLayout';
import { Login } from './components/Login';
import { ProtectedRoute } from './components/ProtectedRoute';
import AdminUsers from './components/AdminUsers';

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<Login />} />

        {/* Protected Routes with MainLayout */}
        <Route element={<ProtectedRoute><MainLayout /></ProtectedRoute>}>
          <Route path="/" element={<HomePage />} />
          <Route path="/info" element={<SystemInfoPage />} />
          <Route path="/ai-test" element={<AITestPage />} />
          <Route path="/gerador-quesitos" element={<PaginaGeradorQuesitos />} />
          <Route path="/admin/users" element={<AdminUsers />} />
        </Route>

        {/* Redirect root to login */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
