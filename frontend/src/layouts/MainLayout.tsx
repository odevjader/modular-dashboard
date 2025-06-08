// frontend/src/layouts/MainLayout.tsx
import React, { useState, useMemo } from 'react';
import { Outlet, Link as RouterLink, useLocation, useNavigate } from 'react-router-dom';
// import { mainNavItems } from '../config/navigation'; // Static navigation removed for sidebar
// import { getIconComponent } from '../utils/iconMap'; // Not needed if FrontendModule.icon is component itself
import {
  AppBar, Toolbar, Typography, Box, Drawer, List, ListItem, ListItemButton,
  ListItemIcon, ListItemText, IconButton, useTheme, useMediaQuery, CssBaseline, Icon,
  Collapse, Button, Link
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import { useAuthStore } from '../stores/authStore';
import { APP_MODULES, FrontendModule } from '../config/moduleRegistry'; // Import new module registry

// Interface for items used by NavListItems - can be simplified if only for dynamic modules
interface DisplayNavItem {
  key: string;
  label: string;
  path?: string;
  icon?: React.ElementType; // MUI SvgIcon compatible
  children?: DisplayNavItem[];
  onClick?: () => void;
  selected?: boolean;
}

const drawerWidth = 240; // Define drawerWidth for use in component styles

const DynamicNavListItems: React.FC<{
  items: DisplayNavItem[],
  isMobile: boolean,
  handleDrawerToggle: () => void,
  level?: number
}> = ({ items, isMobile, handleDrawerToggle, level = 0 }) => {
  const location = useLocation();
  const [openItems, setOpenItems] = useState<{ [key: string]: boolean }>({});

  const handleCollapseToggle = (label: string) => {
    setOpenItems(prev => ({ ...prev, [label]: !prev[label] }));
  };

  if (items.length === 0 && level === 0) {
    return null; // No items to display
  }

  return (
    <List sx={{ pl: level * 2 }}>
      {items.map((item) => {
        const IconComponent = item.icon;
        // For children, selected state is handled by parent click or if a child is active.
        // For simplicity, direct path match for selection here.
        const isActive = item.path ? location.pathname === item.path && !item.children : false;
        const isOpen = openItems[item.label] || false;

        if (item.children && item.children.length > 0) {
          return (
            <React.Fragment key={item.key}>
              <ListItemButton onClick={() => handleCollapseToggle(item.label)}>
                {IconComponent && (
                  <ListItemIcon sx={{ minWidth: '40px' }}>
                    <IconComponent />
                  </ListItemIcon>
                )}
                <ListItemText primary={item.label} />
                {isOpen ? <ExpandLess /> : <ExpandMore />}
              </ListItemButton>
              <Collapse in={isOpen} timeout="auto" unmountOnExit>
                <DynamicNavListItems
                  items={item.children}
                  isMobile={isMobile}
                  handleDrawerToggle={handleDrawerToggle}
                  level={level + 1}
                />
              </Collapse>
            </React.Fragment>
          );
        }

        if (item.path && item.path !== '#') {
          return (
            <ListItem key={item.key} disablePadding>
              <ListItemButton
                component={RouterLink}
                to={item.path}
                selected={item.selected !== undefined ? item.selected : isActive}
                onClick={isMobile ? handleDrawerToggle : undefined}
              >
                {IconComponent && (
                  <ListItemIcon sx={{ minWidth: '40px' }}>
                    <IconComponent color={isActive ? 'primary' : 'inherit'} />
                  </ListItemIcon>
                )}
                <ListItemText primary={item.label} />
              </ListItemButton>
            </ListItem>
          );
        }
        // For items with onClick (like a group header that's not a link)
        if (item.onClick && !item.path) {
             return (
                <ListItemButton key={item.key} onClick={item.onClick}>
                    {IconComponent && (
                        <ListItemIcon sx={{ minWidth: '40px' }}>
                            <IconComponent />
                        </ListItemIcon>
                    )}
                    <ListItemText primary={item.label} />
                    {/* Optional: Add expand/collapse icon if children are manually handled via onClick */}
                </ListItemButton>
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
  const { logout, user } = useAuthStore(); // Get user for role checking
  const navigate = useNavigate();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // --- Dynamic Sidebar Item Generation ---
  const sidebarNavItems = useMemo(() => {
    const userRoles = user?.roles || (user?.role ? (Array.isArray(user.role) ? user.role : [user.role]) : []);

    return APP_MODULES
      .filter(module => {
        if (!module.showInNav) return false;
        if (module.requiredRole) {
          const roles = Array.isArray(module.requiredRole) ? module.requiredRole : [module.requiredRole];
          return roles.some(role => userRoles.includes(role));
        }
        return true; // No specific role required, show to all authenticated users
      })
      .map((module: FrontendModule): DisplayNavItem => ({
        key: module.id,
        label: module.name,
        path: module.path,
        icon: module.icon, // Already a component
        // children: undefined, // Add logic here if grouping is desired based on module.group
      }));
  }, [user]); // Recalculate if user (and thus roles) changes


  // --- Static App Bar Items (can still come from navigation.ts or be hardcoded if few) ---
  // For simplicity, let's keep app bar items minimal or also make them dynamic if needed.
  // The original `mainNavItems` from `navigation.ts` could still be used for app bar or homepage buttons
  // if its structure is maintained or adapted. For now, focusing on sidebar.
  // Example: Hardcoded App Bar items or fetch from a different config
  const appBarItems: Array<{path: string, label: string}> = [
    // { path: "/info", label: "System Info"}, // Example, if System Info is always in app bar
  ];
   // Let's try to get appBarItems from the static navigation.ts for now, filtering by showInAppBar
   // This requires re-introducing mainNavItems for this specific purpose or creating a new config.
   // For now, we'll leave appBarItems empty to focus on dynamic sidebar.
   // If `navigation.ts` is to be kept for other nav elements, it should be imported.
   // import { mainNavItems as staticNavItems } from '../config/navigation';
   // const appBarItems = staticNavItems.filter(item => item.showInAppBar && !item.children);


  const drawerContent = (
    <div>
      <Toolbar /> {/* For spacing under the AppBar */}
      <DynamicNavListItems items={sidebarNavItems} isMobile={isMobile} handleDrawerToggle={handleDrawerToggle} />
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
            to="/" // Default link for the title
            sx={{
              flexGrow: 1,
              color: 'inherit',
              textDecoration: 'none',
              '&:hover': { textDecoration: 'none' },
            }}
          >
            <Typography variant="h6" noWrap component="div">
              Modular Dashboard {/* App Title */}
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
                Sair ({user?.email || 'User'}) {/* Display user email or a fallback */}
              </Button>
            )}
          </Box>
        </Toolbar>
      </AppBar>
      <Box component="nav" sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }} aria-label="mailbox folders">
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }} // Better mobile performance
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth }
          }}
        >
          {drawerContent}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth }
          }}
          open
        >
          {drawerContent}
        </Drawer>
      </Box>
      <Box component="main" sx={{ flexGrow: 1, p: 3, width: { sm: `calc(100% - ${drawerWidth}px)` } }}>
        <Toolbar /> {/* Ensure content is below AppBar */}
        <Outlet /> {/* This is where the routed page components will render */}
      </Box>
    </Box>
  );
};

export default MainLayout;