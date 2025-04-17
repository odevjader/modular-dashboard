// frontend/src/layouts/MainLayout.tsx
import React, { useState } from 'react';
import { Outlet, Link as RouterLink, useLocation } from 'react-router-dom';
import { mainNavItems } from '../config/navigation'; // Import the navigation config
import { getIconComponent } from '../utils/iconMap'; // Import the icon mapping utility
import {
  AppBar, Toolbar, Typography, Box, Drawer, List, ListItem, ListItemButton,
  ListItemIcon, ListItemText, IconButton, useTheme, useMediaQuery, CssBaseline, Icon
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu'; // Menu icon for mobile drawer

const drawerWidth = 240; // Define standard drawer width

const MainLayout: React.FC = () => {
  const theme = useTheme();
  // Check if the screen is small (mobile breakpoint)
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  // State to control mobile drawer open/close
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation(); // Get current location for active link styling

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  // Filter navigation items for sidebar and appbar
  const sidebarItems = mainNavItems.filter(item => item.showInSidebar);
  const appBarItems = mainNavItems.filter(item => item.showInAppBar);

  // Content of the drawer (navigation list)
  const drawerContent = (
    <div>
      <Toolbar /> {/* Necessary spacer to position content below AppBar */}
      <List>
        {sidebarItems.map((item) => {
          const IconComponent = getIconComponent(item.icon);
          const isActive = location.pathname === item.path;
          return (
            <ListItem key={item.label} disablePadding>
              <ListItemButton
                component={RouterLink}
                to={item.path}
                selected={isActive} // Highlight active link
                onClick={isMobile ? handleDrawerToggle : undefined} // Close mobile drawer on click
                sx={{ // Custom styling for active item
                  '&.Mui-selected': {
                    // backgroundColor: theme.palette.action.selected, // Default selection color
                    // '&:hover': {
                    //   backgroundColor: theme.palette.action.hover,
                    // },
                  },
                }}
              >
                <ListItemIcon sx={{ minWidth: '40px' }}> {/* Adjust icon padding if needed */}
                  {/* Render the mapped icon component */}
                  <Icon component={IconComponent} color={isActive ? 'primary' : 'inherit'} />
                </ListItemIcon>
                <ListItemText primary={item.label} />
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>
    </div>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline /> {/* Ensures consistent baseline styles */}
      {/* AppBar */}
      <AppBar
        position="fixed"
        sx={{
          // Only extend app bar width beyond drawer on larger screens
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` }, // Margin-left to accommodate drawer on larger screens
        }}
      >
        <Toolbar>
          {/* Menu button - only shown on mobile */}
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }} // Only display on small screens ('xs', 'sm' threshold)
          >
            <MenuIcon />
          </IconButton>

          <Typography variant="h6" noWrap component="div">
            Modular Dashboard
          </Typography>
        </Toolbar>
      </AppBar>
      {/* Drawer for navigation (hidden on larger screens) */}
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
        aria-label="mailbox folders"
      >
        {/* The implementation can be swapped with js to avoid SEO duplication of links. */}
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawerContent}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawerContent}
        </Drawer>
      </Box>
      <Box
        component="main"
        sx={{ flexGrow: 1, p: 3, width: { sm: `calc(100% - ${drawerWidth}px)` } }}
      >
        <Toolbar /> {/* Toolbar spacer */}
        <Outlet /> {/* Render the child routes */}
      </Box>
    </Box>
  );
};

export default MainLayout;