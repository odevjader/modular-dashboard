// frontend/src/App.tsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import SystemInfoPage from './pages/SystemInfoPage';
import AITestPage from './pages/AITestPage'; // ADDED: Import the new AI Test page
import MainLayout from './layouts/MainLayout';

function App() {
  return (
    <Router>
      <Routes>
        {/* Routes with MainLayout */}
        <Route element={<MainLayout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/info" element={<SystemInfoPage />} />
          {/* ADDED: Route for AI Test Page */}
          <Route path="/ai-test" element={<AITestPage />} />
        </Route>

        {/* Routes without MainLayout (e.g., Login page) can go here if needed */}

        {/* Catch-all route for 404 Not Found (optional) */}
      </Routes>
    </Router>
  );
}

export default App;
