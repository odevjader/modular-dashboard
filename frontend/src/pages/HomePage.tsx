// frontend/src/pages/HomePage.tsx
import React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

const HomePage: React.FC = () => {
  return (
    <Box sx={{ my: 4 }}> {/* Add some vertical margin */}
      <Typography variant="h4" component="h1" gutterBottom>
        Welcome to the Dashboard!
      </Typography>
      <Typography variant="body1">
        This is the placeholder home page. Content and features will be added here.
      </Typography>
      {/* You can add more components or content here later */}
    </Box>
  );
};

export default HomePage;