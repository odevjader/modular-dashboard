// frontend/src/layouts/MainLayout.tsx
import React from 'react';
import { Outlet } from 'react-router-dom';
import { Box, AppBar, Toolbar, Typography, Container } from '@mui/material';

const MainLayout: React.FC = () => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* AppBar */}
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Modular Dashboard
          </Typography>
          {/* Add other AppBar items like buttons or user menu here later */}
        </Toolbar>
      </AppBar>

      {/* Main Content Area */}
      <Container component="main" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
        {/* Outlet renders the matched child route component (e.g., HomePage) */}
        <Outlet />
      </Container>

      {/* Optional Footer */}
      <Box
        component="footer"
        sx={{
          py: 2, // Padding top and bottom
          px: 2, // Padding left and right
          mt: 'auto', // Pushes footer to the bottom
          backgroundColor: (theme) =>
            theme.palette.mode === 'light'
              ? theme.palette.grey[200]
              : theme.palette.grey[800],
        }}
      >
        <Container maxWidth="sm">
          <Typography variant="body2" color="text.secondary" align="center">
            {'Copyright © Modular Dashboard '}
            {new Date().getFullYear()}
            {'.'}
          </Typography>
        </Container>
      </Box>
    </Box>
  );
};

export default MainLayout;