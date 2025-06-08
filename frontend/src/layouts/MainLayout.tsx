import React from 'react';
import { Outlet, Link as RouterLink, useNavigate } from 'react-router-dom';
import { styled, useTheme, Theme } from '@mui/material/styles'; // Added Theme
import {
  AppBar as MuiAppBarCore,
  Toolbar, Typography, Box, Drawer as MuiDrawerCore, List, ListItem, ListItemButton,
  ListItemIcon, ListItemText, IconButton, CssBaseline, Tooltip
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
// import ChevronRightIcon from '@mui/icons-material/ChevronRight'; // Not used in provided example if drawer closes only to left
import HomeIcon from '@mui/icons-material/Home';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import LogoutIcon from '@mui/icons-material/Logout';

import { useAuthStore } from '../stores/authStore';
import { getModuleRegistry, ModuleConfig } from '../config/moduleRegistry';
import { SvgIconComponent } from '@mui/icons-material';

const drawerWidth = 240;

const MuiAppBar = styled(MuiAppBarCore, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }: { theme: Theme, open: boolean }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const MuiDrawer = styled(MuiDrawerCore, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }: { theme: Theme, open: boolean }) => ({
    '& .MuiDrawer-paper': {
      position: 'relative',
      whiteSpace: 'nowrap',
      width: drawerWidth,
      transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
      }),
      boxSizing: 'border-box',
      ...(!open && {
        overflowX: 'hidden',
        transition: theme.transitions.create('width', {
          easing: theme.transitions.easing.sharp,
          duration: theme.transitions.duration.leavingScreen,
        }),
        width: theme.spacing(7),
        [theme.breakpoints.up('sm')]: {
          width: theme.spacing(9),
        },
      }),
    },
  }),
);


const MainLayout: React.FC = () => {
  const theme = useTheme(); // useTheme must be called within the component
  const [open, setOpen] = React.useState(true);

  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const moduleRegistry = getModuleRegistry();

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Determine user role for filtering. Adapt if user.role is an array e.g. user.roles.includes('ADMIN')
  const isAdmin = user?.role === 'admin'; // Changed to lowercase 'admin'

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <MuiAppBar position="absolute" open={open}>
        <Toolbar
          sx={{
            pr: '24px',
          }}
        >
          <IconButton
            edge="start"
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            sx={{
              marginRight: '36px',
              ...(open && { display: 'none' }),
            }}
          >
            <MenuIcon />
          </IconButton>
          <Typography
            component="h1"
            variant="h6"
            color="inherit"
            noWrap
            sx={{ flexGrow: 1 }}
          >
            Modular Dashboard
          </Typography>
          <Tooltip title="Logout">
            <IconButton color="inherit" onClick={handleLogout}>
              <LogoutIcon />
            </IconButton>
          </Tooltip>
        </Toolbar>
      </MuiAppBar>
      <MuiDrawer variant="permanent" open={open}>
        <Toolbar
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'flex-end',
            px: [1],
          }}
        >
          <IconButton onClick={handleDrawerClose}>
            <ChevronLeftIcon />
          </IconButton>
        </Toolbar>
        <Box sx={{ overflowY: 'auto', overflowX: 'hidden', height: 'calc(100% - 64px)' }}> {/* Adjust height based on Toolbar */}
          <List component="nav">
            <ListItem disablePadding sx={{ display: 'block' }}>
              <Tooltip title={open ? "" : "Home"} placement="right">
                <ListItemButton
                  component={RouterLink}
                  to="/"
                  sx={{
                    minHeight: 48,
                    justifyContent: open ? 'initial' : 'center',
                    px: 2.5,
                  }}
                >
                  <ListItemIcon
                    sx={{
                      minWidth: 0,
                      mr: open ? 3 : 'auto',
                      justifyContent: 'center',
                    }}
                  >
                    <HomeIcon />
                  </ListItemIcon>
                  <ListItemText primary="Home" sx={{ opacity: open ? 1 : 0 }} />
                </ListItemButton>
              </Tooltip>
            </ListItem>

            {Object.values(moduleRegistry).filter(module => !module.adminOnly || (module.adminOnly && isAdmin)).map((module: ModuleConfig) => {
              const IconComponent = module.navIcon as SvgIconComponent | undefined;
              return (
                <ListItem key={module.name} disablePadding sx={{ display: 'block' }}>
                  <Tooltip title={open ? "" : (module.navText || module.name)} placement="right">
                    <ListItemButton
                      component={RouterLink}
                      to={module.basePath}
                      sx={{
                        minHeight: 48,
                        justifyContent: open ? 'initial' : 'center',
                        px: 2.5,
                      }}
                    >
                      <ListItemIcon
                        sx={{
                          minWidth: 0,
                          mr: open ? 3 : 'auto',
                          justifyContent: 'center',
                        }}
                      >
                        {IconComponent ? <IconComponent /> : <div style={{ width: 24, height: 24 }} /> }
                      </ListItemIcon>
                      <ListItemText primary={module.navText || module.name} sx={{ opacity: open ? 1 : 0 }} />
                    </ListItemButton>
                  </Tooltip>
                </ListItem>
              );
            })}
          </List>
          {isAdmin && (
            <>
              <Box sx={{ my: 1, mx: open ? 2.5 : 'auto', pl: open ? 0 : 1.5 }}><Typography variant="caption" sx={{ opacity: open ? 0.7 : 0 }}>Admin</Typography></Box>
              <List component="nav">
                <ListItem disablePadding sx={{ display: 'block' }}>
                  <Tooltip title={open ? "" : "Admin Users"} placement="right">
                    <ListItemButton
                      component={RouterLink}
                      to="/admin/users"
                      sx={{
                        minHeight: 48,
                        justifyContent: open ? 'initial' : 'center',
                        px: 2.5,
                      }}
                    >
                      <ListItemIcon
                        sx={{
                          minWidth: 0,
                          mr: open ? 3 : 'auto',
                          justifyContent: 'center',
                        }}
                      >
                        <AdminPanelSettingsIcon />
                      </ListItemIcon>
                      <ListItemText primary="Admin Users" sx={{ opacity: open ? 1 : 0 }} />
                    </ListItemButton>
                  </Tooltip>
                </ListItem>
              </List>
            </>
          )}
        </Box>
      </MuiDrawer>
      <Box
        component="main"
        sx={{
          backgroundColor: (theme) => // theme is accessible here
            theme.palette.mode === 'light'
              ? theme.palette.grey[100]
              : theme.palette.grey[900],
          flexGrow: 1,
          height: '100vh',
          overflow: 'auto',
        }}
      >
        <Toolbar />
        <Box sx={{ p: 3 }}>
          <Outlet />
        </Box>
      </Box>
    </Box>
  );
};

export default MainLayout;