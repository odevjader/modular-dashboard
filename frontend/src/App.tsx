// frontend/src/App.tsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import SystemInfoPage from './pages/SystemInfoPage'; // ADDED: Import the new page
import MainLayout from './layouts/MainLayout';

function App() {
  return (
    <Router>
      <Routes>
        {/* Routes with MainLayout */}
        <Route element={<MainLayout />}>
          <Route path="/" element={<HomePage />} />
          {/* ADDED: Route for System Info Page */}
          <Route path="/info" element={<SystemInfoPage />} />
        </Route>

        {/* Routes without MainLayout (e.g., Login page) can go here if needed */}

        {/* Catch-all route for 404 Not Found (optional) */}
      </Routes>
    </Router>
  );
}

export default App;
