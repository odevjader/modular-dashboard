// frontend/src/layouts/MainLayout.tsx
import React from 'react';
import { Outlet, Link as RouterLink } from 'react-router-dom'; // Import RouterLink
import { Box, AppBar, Toolbar, Typography, Container, Button } from '@mui/material'; // Import Button

const MainLayout: React.FC = () => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* AppBar */}
      <AppBar position="static">
        <Toolbar>
          {/* Wrap title in a Link to navigate home */}
          <Typography variant="h6" component={RouterLink} to="/" sx={{ flexGrow: 1, color: 'inherit', textDecoration: 'none' }}>
            Modular Dashboard
          </Typography>

          {/* Navigation Links */}
          <Button color="inherit" component={RouterLink} to="/">
            Home
          </Button>
          {/* ADDED: Link to System Info Page */}
          <Button color="inherit" component={RouterLink} to="/info">
            System Info
          </Button>
          {/* Add other AppBar items like buttons or user menu here later */}

        </Toolbar>
      </AppBar>

      {/* Main Content Area */}
      <Container component="main" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
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