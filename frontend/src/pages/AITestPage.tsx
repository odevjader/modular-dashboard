// frontend/src/pages/AITestPage.tsx
import React from 'react';
import AITestInterface from '../modules/ai_test/AITestInterface'; // Import the UI component
import { Container, Typography } from '@mui/material';

const AITestPage: React.FC = () => {
  return (
    <Container maxWidth="md"> {/* Constrain width for better readability */}
      {/* Optional: Add a page title if desired */}
      {/* <Typography variant="h4" component="h1" sx={{ my: 3 }}>
        AI Test Module
      </Typography> */}
      <AITestInterface />
    </Container>
  );
};

export default AITestPage;