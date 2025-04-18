// frontend/src/pages/HomePage.tsx
import React, { useState, useEffect } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Grid, Card, CardActionArea, Typography, Box, Icon } from '@mui/material';
import { mainNavItems } from '../config/navigation';
import { funnyHomepageTitles } from '../config/phrases';
import { getIconComponent } from '../utils/iconMap';

const HomePage: React.FC = () => {
  const [pageTitle, setPageTitle] = useState<string>("Dashboard Modules");

  useEffect(() => {
    const randomIndex = Math.floor(Math.random() * funnyHomepageTitles.length);
    setPageTitle(funnyHomepageTitles[randomIndex]);
  }, []);

  // Filter items to show on the homepage
  const homepageItems = mainNavItems.filter(item => item.showOnHomepage);
  // --- ADDED DEBUG LOG ---
  console.log('HomePage - Items filtered for homepage:', homepageItems);
  // --- END DEBUG LOG ---

  return (
    <Box sx={{ flexGrow: 1, p: 2 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center" sx={{ mb: 4 }}>
        {pageTitle}
      </Typography>
      {homepageItems.length > 0 ? (
        <Grid container spacing={3} justifyContent="center">
          {homepageItems.map((item) => {
            const ModuleIcon = getIconComponent(item.icon);
            return (
              <Grid item key={item.path + item.label} xs={12} sm={6} md={4} lg={3}> {/* Added label to key for uniqueness */}
                <Card
                  elevation={3}
                  sx={{
                    height: '100%',
                    display: 'flex',
                    maxWidth: 300,
                    margin: 'auto',
                  }}
                >
                  <CardActionArea
                    component={RouterLink}
                    to={item.path}
                    sx={{
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'center',
                      alignItems: 'center',
                      p: 3,
                      flexGrow: 1,
                    }}
                  >
                    <Icon component={ModuleIcon} sx={{ fontSize: 50, mb: 2 }} color="primary" />
                    <Typography variant="h6" component="div" align="center" sx={{ lineHeight: 1.3 }}>
                      {item.label}
                    </Typography>
                  </CardActionArea>
                </Card>
              </Grid>
            );
          })}
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