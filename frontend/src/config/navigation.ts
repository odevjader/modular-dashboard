// frontend/src/config/navigation.ts
// REMOVED: import React from 'react'; - Not needed here

// Define the type for a navigation item, now including display flags and icon identifier
export interface NavItem {
  path: string;        // URL path (e.g., '/info')
  label: string;       // Text label (e.g., 'System Info')
  icon: string;        // MUI Icon name string identifier (e.g., 'Info', 'Home')
  showOnHomepage: boolean; // Show big text button on '/'?
  showInSidebar: boolean;  // Show in sidebar menu?
  showInAppBar: boolean;   // Show link/button in top AppBar?
}

// Define the main navigation items / dashboard modules
export const mainNavItems: NavItem[] = [
  {
    path: '/',
    label: 'Home',
    icon: 'Home',
    showOnHomepage: false,
    showInSidebar: true,
    showInAppBar: true,
  },
  {
    path: '/info',
    label: 'System Info',
    icon: 'Info',
    showOnHomepage: true,
    showInSidebar: true,
    showInAppBar: true,
  },
  // Future modules will add their items here, setting flags as needed
];