// frontend/src/layouts/MainLayout.tsx
import React, { useState } from 'react';
// Import Link as RouterLink
import { Outlet, Link as RouterLink, useLocation } from 'react-router-dom';
import { mainNavItems } from '../config/navigation';
import { getIconComponent } from '../utils/iconMap';
import {
  AppBar, Toolbar, Typography, Box, Drawer, List, ListItem, ListItemButton,
  ListItemIcon, ListItemText, IconButton, useTheme, useMediaQuery, CssBaseline, Icon,
  Collapse, Button, Link // Import MUI Link
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';

const drawerWidth = 240;

// Helper component to render list items recursively (remains the same)
const NavListItems: React.FC<{ items: NavItem[], isMobile: boolean, handleDrawerToggle: () => void, level?: number }> =
  ({ items, isMobile, handleDrawerToggle, level = 0 }) => {
  const location = useLocation();
  const [openItems, setOpenItems] = useState<{ [key: string]: boolean }>({});

  const handleCollapseToggle = (label: string) => {
    setOpenItems(prev => ({ ...prev, [label]: !prev[label] }));
  };

  // Filter items that should actually be shown in the sidebar at this level
  const itemsToShow = items.filter(item => item.showInSidebar);
  if (itemsToShow.length === 0 && level === 0) { // Avoid logging if top-level is empty
       console.log('MainLayout - No top-level items configured for sidebar.');
       return null;
  }


  return (
    <List sx={{ pl: level * 2 }}>
      {itemsToShow.map((item) => {
        const IconComponent = getIconComponent(item.icon);
        const isActive = location.pathname === item.path && !item.children;
        const isOpen = openItems[item.label] || false;

        // console.log(`MainLayout - Rendering Sidebar Item (Level ${level}):`, item.label, item);

        // If item has children, render it as a collapsible group
        if (item.children && item.children.length > 0) {
          // Filter children that should actually be shown in the sidebar
          const visibleChildren = item.children.filter(child => child.showInSidebar);
          // Only render the parent if it has visible children to show
          if (visibleChildren.length === 0) return null;

          return (
            <React.Fragment key={item.label}>
              <ListItemButton onClick={() => handleCollapseToggle(item.label)}>
                <ListItemIcon sx={{ minWidth: '40px' }}>
                  <Icon component={IconComponent} />
                </ListItemIcon>
                <ListItemText primary={item.label} />
                {isOpen ? <ExpandLess /> : <ExpandMore />}
              </ListItemButton>
              <Collapse in={isOpen} timeout="auto" unmountOnExit>
                {/* Recursively render child items */}
                <NavListItems items={visibleChildren} isMobile={isMobile} handleDrawerToggle={handleDrawerToggle} level={level + 1} />
              </Collapse>
            </React.Fragment>
          );
        }

        // Otherwise, render a regular navigation link (if it's not just a group header)
        // Ensure path is not '#' if it's meant to be a direct link
        if (item.path && item.path !== '#') {
            return (
              <ListItem key={item.label} disablePadding>
                <ListItemButton component={RouterLink} to={item.path} selected={isActive} onClick={isMobile ? handleDrawerToggle : undefined}>
                  <ListItemIcon sx={{ minWidth: '40px' }}>
                    <Icon component={IconComponent} color={isActive ? 'primary' : 'inherit'} />
                  </ListItemIcon>
                  <ListItemText primary={item.label} />
                </ListItemButton>
              </ListItem>
            );
        }
        // If it's an item with no children shown in sidebar but path is '#', don't render as link
        return null;

      })}
    </List>
  );
};


const MainLayout: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  // Filter items for sidebar (top level only) and appbar
  const sidebarTopLevelItems = mainNavItems.filter(item => item.showInSidebar);
  // Filter for AppBar: must have showInAppBar=true AND NOT have children (usually)
  const appBarItems = mainNavItems.filter(item => item.showInAppBar && !item.children);

  // console.log('MainLayout - Filtered Sidebar Top-Level Items:', sidebarTopLevelItems);
  // console.log('MainLayout - Filtered AppBar Items:', appBarItems);

  const drawerContent = (
    <div>
      <Toolbar /> {/* Spacer */}
      <NavListItems items={sidebarTopLevelItems} isMobile={isMobile} handleDrawerToggle={handleDrawerToggle} />
    </div>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      {/* AppBar */}
      <AppBar
        position="fixed"
        sx={{ width: { sm: `calc(100% - ${drawerWidth}px)` }, ml: { sm: `${drawerWidth}px` } }}
      >
        <Toolbar>
          <IconButton
            color="inherit" aria-label="open drawer" edge="start"
            onClick={handleDrawerToggle} sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>

          {/* Wrap Typography title in a Link component */}
          <Link
            component={RouterLink}
            to="/"
            sx={{
              flexGrow: 1,
              color: 'inherit', // Inherit color from AppBar
              textDecoration: 'none', // Remove underline
              '&:hover': {
                  textDecoration: 'none', // Ensure no underline on hover
              },
            }}
          >
            <Typography variant="h6" noWrap component="div">
              Dashboard
            </Typography>
          </Link>

          {/* Render AppBar items */}
          <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
            {appBarItems.map((item) => (
              <Button
                key={item.path} color="inherit" component={RouterLink} to={item.path}
              >
                {item.label}
              </Button>
            ))}
          </Box>
        </Toolbar>
      </AppBar>

      {/* Sidebar (Drawer) */}
      <Box component="nav" sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}>
        <Drawer
          variant="temporary" open={mobileOpen} onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{ display: { xs: 'block', sm: 'none' }, '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth } }}
        >
          {drawerContent}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{ display: { xs: 'none', sm: 'block' }, '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth } }}
          open
        >
          {drawerContent}
        </Drawer>
      </Box>

      {/* Main Content Area */}
      <Box component="main" sx={{ flexGrow: 1, p: 3, width: { sm: `calc(100% - ${drawerWidth}px)` } }}>
        <Toolbar /> {/* Spacer */}
        <Outlet />
      </Box>
    </Box>
  );
};

export default MainLayout;