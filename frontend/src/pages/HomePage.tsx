// frontend/src/pages/HomePage.tsx
import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Grid, Button, Typography, Box, Paper } from '@mui/material';
import { mainNavItems } from '../config/navigation'; // Import the config

const HomePage: React.FC = () => {
  // Filter items to show on the homepage
  const homepageItems = mainNavItems.filter(item => item.showOnHomepage);

  return (
    <Box sx={{ flexGrow: 1, p: 2 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center" sx={{ mb: 4 }}>
        Dashboard Modules
      </Typography>
      {homepageItems.length > 0 ? (
        <Grid container spacing={4} justifyContent="center">
          {homepageItems.map((item) => (
            <Grid item key={item.path} xs={12} sm={6} md={4} lg={3}> {/* Adjust grid sizing */}
              {/* Using Paper and Button for a larger clickable area */}
              <Paper elevation={3} sx={{ height: '150px', display: 'flex' }}>
                <Button
                  component={RouterLink}
                  to={item.path}
                  variant="contained" // Use contained for a prominent button look
                  color="primary" // Or "secondary", "inherit", etc.
                  sx={{
                    width: '100%',
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column', // Arrange text vertically if needed
                    justifyContent: 'center',
                    alignItems: 'center',
                    textAlign: 'center',
                    fontSize: '1.1rem', // Larger text
                    p: 2,
                  }}
                >
                  {item.label}
                </Button>
              </Paper>
              {/* Alternative: Using Card
              <Card sx={{ height: '150px', display: 'flex' }}>
                <CardActionArea
                  component={RouterLink}
                  to={item.path}
                  sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}
                >
                  <CardContent sx={{ textAlign: 'center' }}>
                    <Typography gutterBottom variant="h5" component="div">
                      {item.label}
                    </Typography>
                  </CardContent>
                </CardActionArea>
              </Card>
              */}
            </Grid>
          ))}
        </Grid>
      ) : (
        <Typography align="center" sx={{ mt: 5 }}>
          No modules configured to display on the homepage.
        </Typography>
      )}
    </Box>
  );
};

export default HomePage;