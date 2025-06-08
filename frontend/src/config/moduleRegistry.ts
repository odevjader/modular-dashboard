// frontend/src/config/moduleRegistry.ts
import { ComponentType, LazyExoticComponent, lazy } from 'react';
import { SvgIconProps } from '@mui/material/SvgIcon';

// --- Icon Imports ---
// Import specific MUI icons or custom SVG components.
// Using MUI icons as examples. Ensure these are installed or replace with your actual icons.
import InfoIcon from '@mui/icons-material/Info';
import ScienceIcon from '@mui/icons-material/Science'; // For AI Test
import DescriptionIcon from '@mui/icons-material/Description'; // For Gerador Quesitos
import HomeIcon from '@mui/icons-material/Home';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings'; // For Admin Users

// --- Module Interface ---
// Defines the shape of a frontend module configuration object.
export interface FrontendModule {
  id: string; // Unique identifier (e.g., 'home', 'system-info', 'ai-test')
  path: string; // React Router path (e.g., '/', '/info', '/ai-test')
  name: string; // Human-readable name for navigation and titles (e.g., 'Home', 'System Info')

  // Lazy loaded component for the module's main page/view
  // Ensures that module code is split and loaded on demand.
  component: LazyExoticComponent<ComponentType<any>>;

  // Icon for navigation (Material UI SvgIcon compatible)
  // Store the component itself, not a string.
  icon?: ComponentType<SvgIconProps>;

  // Whether to show this module in the main navigation (e.g., sidebar)
  showInNav: boolean;

  // Optional: Required role to access this module. Used by ProtectedRoute.
  // If undefined, accessible to all authenticated users.
  // If defined, ProtectedRoute should check against user's role.
  requiredRole?: string | string[]; // e.g., 'ADMIN', ['EDITOR', 'ADMIN']

  // Optional: For grouping in navigation or other UI purposes
  group?: string;
}

// --- Module Definitions ---
// Manually define the frontend modules available in the application.
// For V1, this is a static list. Future versions could load this from a manifest.

// Note on lazy loading paths:
// These paths are relative to the `src/pages` or `src/modules` directory.
// Vite supports dynamic imports with variables if they follow a certain pattern,
// but for full type safety and clarity with `lazy`, direct static strings are more robust here.

export const APP_MODULES: FrontendModule[] = [
  {
    id: 'home',
    path: '/',
    name: 'Home',
    component: lazy(() => import('../pages/HomePage')),
    icon: HomeIcon,
    showInNav: true,
  },
  {
    id: 'system-info',
    path: '/info',
    name: 'System Info',
    component: lazy(() => import('../pages/SystemInfoPage')),
    icon: InfoIcon,
    showInNav: true,
  },
  {
    id: 'ai-test',
    path: '/ai-test',
    name: 'AI Test',
    component: lazy(() => import('../pages/AITestPage')),
    icon: ScienceIcon,
    showInNav: true,
  },
  {
    id: 'gerador-quesitos',
    path: '/gerador-quesitos',
    name: 'Gerador Quesitos',
    component: lazy(() => import('../pages/PaginaGeradorQuesitos')),
    icon: DescriptionIcon,
    showInNav: true,
  },
  {
    id: 'admin-users',
    path: '/admin/users',
    name: 'Manage Users',
    // Assuming AdminUsers is a page/component that can be lazy loaded.
    // If it's small or already part of a larger chunk, direct import might be fine,
    // but lazy loading is good practice for consistency.
    component: lazy(() => import('../components/AdminUsers')), // Path might be '../components/AdminUsers'
    icon: AdminPanelSettingsIcon,
    showInNav: true, // Show in nav only for admin users (logic to be handled in nav component)
    requiredRole: 'ADMIN', // Example: Only accessible by users with 'ADMIN' role
  },
  // Example of a module not shown in navigation but routable:
  // {
  //   id: 'user-profile',
  //   path: '/profile/:userId',
  //   name: 'User Profile',
  //   component: lazy(() => import('../pages/UserProfilePage')),
  //   showInNav: false,
  // },
];

// --- Helper Functions (Optional) ---

/**
 * Finds a module by its ID.
 * @param id The ID of the module to find.
 * @returns The module configuration or undefined if not found.
 */
export const getModuleById = (id: string): FrontendModule | undefined => {
  return APP_MODULES.find(module => module.id === id);
};

/**
 * Finds a module by its path.
 * @param path The path of the module to find.
 * @returns The module configuration or undefined if not found.
 */
export const getModuleByPath = (path: string): FrontendModule | undefined => {
  return APP_MODULES.find(module => module.path === path);
};

/**
 * Filters modules that should be shown in navigation.
 * Optionally, can be enhanced to filter by user roles if needed at this stage,
 * though role-based rendering is often handled directly in the navigation component.
 * @returns An array of modules to be displayed in navigation.
 */
export const getNavigableModules = (userRoles?: string[]): FrontendModule[] => {
  return APP_MODULES.filter(module => {
    if (!module.showInNav) {
      return false;
    }
    // If userRoles are provided, check against module.requiredRole
    if (userRoles && module.requiredRole) {
      const roles = Array.isArray(module.requiredRole) ? module.requiredRole : [module.requiredRole];
      if (!roles.some(role => userRoles.includes(role))) {
        return false; // User does not have any of the required roles
      }
    }
    return true;
  });
};

// Ensure MUI icons are installed if you are using them:
// npm install @mui/icons-material @mui/material @emotion/react @emotion/styled
// or
// yarn add @mui/icons-material @mui/material @emotion/react @emotion/styled

// If AdminUsers.tsx is in 'pages' directory:
// component: lazy(() => import('../pages/AdminUsersPage')), // assuming you rename/move it

// Check paths for lazy loaded components. For example, if AdminUsers is actually a page:
// Change: component: lazy(() => import('../components/AdminUsers')),
// To:     component: lazy(() => import('../pages/AdminUsersPage')), // if you create/move it to pages
// For now, using the path from original plan (../components/AdminUsers)
