// frontend/src/App.tsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage'; // We will create this page next
import MainLayout from './layouts/MainLayout'; // We will create this layout next
// Import other pages here as they are created
// import AboutPage from './pages/AboutPage';

function App() {
  return (
    <Router>
      <Routes>
        {/* Routes with MainLayout */}
        <Route element={<MainLayout />}>
          <Route path="/" element={<HomePage />} />
          {/* Add other routes that use MainLayout here */}
          {/* Example: <Route path="/about" element={<AboutPage />} /> */}
        </Route>

        {/* Routes without MainLayout (e.g., Login page) can go here if needed */}
        {/* Example: <Route path="/login" element={<LoginPage />} /> */}

        {/* Catch-all route for 404 Not Found (optional) */}
        {/* <Route path="*" element={<NotFoundPage />} /> */}
      </Routes>
    </Router>
  );
}

export default App;
