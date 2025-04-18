// frontend/src/layouts/MainLayout.tsx
import React, { useState } from 'react';
import { Outlet, Link as RouterLink, useLocation } from 'react-router-dom';
import { mainNavItems } from '../config/navigation';
import { getIconComponent } from '../utils/iconMap';
import {
  AppBar, Toolbar, Typography, Box, Drawer, List, ListItem, ListItemButton,
  ListItemIcon, ListItemText, IconButton, useTheme, useMediaQuery, CssBaseline, Icon,
  Collapse, Button // ADDED Button to the import list
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';

const drawerWidth = 240;

// Helper component to render list items recursively
const NavListItems: React.FC<{ items: NavItem[], isMobile: boolean, handleDrawerToggle: () => void, level?: number }> =
  ({ items, isMobile, handleDrawerToggle, level = 0 }) => {
  const location = useLocation();
  const [openItems, setOpenItems] = useState<{ [key: string]: boolean }>({});

  const handleCollapseToggle = (label: string) => {
    setOpenItems(prev => ({ ...prev, [label]: !prev[label] }));
  };

  return (
    <List sx={{ pl: level * 2 }}>
      {items.map((item) => {
        const IconComponent = getIconComponent(item.icon);
        const isActive = location.pathname === item.path && !item.children;
        const isOpen = openItems[item.label] || false;

        // console.log(`MainLayout - Rendering Sidebar Item (Level ${level}):`, item.label, item); // Keep debug log

        if (item.children && item.children.length > 0) {
          const visibleChildren = item.children.filter(child => child.showInSidebar);
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
                <NavListItems items={visibleChildren} isMobile={isMobile} handleDrawerToggle={handleDrawerToggle} level={level + 1} />
              </Collapse>
            </React.Fragment>
          );
        }

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

  const sidebarTopLevelItems = mainNavItems.filter(item => item.showInSidebar);
  const appBarItems = mainNavItems.filter(item => item.showInAppBar && !item.children);

  // console.log('MainLayout - Filtered Sidebar Top-Level Items:', sidebarTopLevelItems); // Keep debug log
  // console.log('MainLayout - Filtered AppBar Items:', appBarItems); // Keep debug log

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
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            Dashboard
          </Typography>
          <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
            {appBarItems.map((item) => ( // Render filtered app bar items
              <Button // This component requires the import
                key={item.path}
                color="inherit"
                component={RouterLink}
                to={item.path}
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