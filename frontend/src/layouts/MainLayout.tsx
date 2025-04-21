// frontend/src/layouts/MainLayout.tsx
import React, { useState } from 'react';
import { Outlet, Link as RouterLink, useLocation, useNavigate } from 'react-router-dom';
import { mainNavItems } from '../config/navigation';
import { getIconComponent } from '../utils/iconMap';
import {
  AppBar, Toolbar, Typography, Box, Drawer, List, ListItem, ListItemButton,
  ListItemIcon, ListItemText, IconButton, useTheme, useMediaQuery, CssBaseline, Icon,
  Collapse, Button, Link
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import { useAuthStore } from '../stores/authStore';

const drawerWidth = 240;

const NavListItems: React.FC<{ items: NavItem[], isMobile: boolean, handleDrawerToggle: () => void, level?: number }> =
  ({ items, isMobile, handleDrawerToggle, level = 0 }) => {
  const location = useLocation();
  const [openItems, setOpenItems] = useState<{ [key: string]: boolean }>({});

  const handleCollapseToggle = (label: string) => {
    setOpenItems(prev => ({ ...prev, [label]: !prev[label] }));
  };

  const itemsToShow = items.filter(item => item.showInSidebar);
  if (itemsToShow.length === 0 && level === 0) {
    console.log('MainLayout - No top-level items configured for sidebar.');
    return null;
  }

  return (
    <List sx={{ pl: level * 2 }}>
      {itemsToShow.map((item) => {
        const IconComponent = getIconComponent(item.icon);
        const isActive = location.pathname === item.path && !item.children;
        const isOpen = openItems[item.label] || false;

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
        return null;
      })}
    </List>
  );
};

const MainLayout: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [mobileOpen, setMobileOpen] = useState(false);
  const { logout, user } = useAuthStore();
  const navigate = useNavigate();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const sidebarTopLevelItems = mainNavItems.filter(item => item.showInSidebar);
  const appBarItems = mainNavItems.filter(item => item.showInAppBar && !item.children);

  const drawerContent = (
    <div>
      <Toolbar />
      <NavListItems items={sidebarTopLevelItems} isMobile={isMobile} handleDrawerToggle={handleDrawerToggle} />
    </div>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{ width: { sm: `calc(100% - ${drawerWidth}px)` }, ml: { sm: `${drawerWidth}px` } }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Link
            component={RouterLink}
            to="/"
            sx={{
              flexGrow: 1,
              color: 'inherit',
              textDecoration: 'none',
              '&:hover': { textDecoration: 'none' },
            }}
          >
            <Typography variant="h6" noWrap component="div">
              Dashboard
            </Typography>
          </Link>
          <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
            {appBarItems.map((item) => (
              <Button
                key={item.path}
                color="inherit"
                component={RouterLink}
                to={item.path}
              >
                {item.label}
              </Button>
            ))}
            {user && (
              <Button color="inherit" onClick={handleLogout}>
                Sair ({user.email})
              </Button>
            )}
          </Box>
        </Toolbar>
      </AppBar>
      <Box component="nav" sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}>
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
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
      <Box component="main" sx={{ flexGrow: 1, p: 3, width: { sm: `calc(100% - ${drawerWidth}px)` } }}>
        <Toolbar />
        <Outlet />
      </Box>
    </Box>
  );
};

export default MainLayout;