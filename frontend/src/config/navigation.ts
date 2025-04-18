// frontend/src/config/navigation.ts

// Define the type for a navigation item, supporting nesting
export interface NavItem {
  path: string;
  label: string;
  icon: string;
  showOnHomepage?: boolean; // Show button on '/' homepage?
  showInSidebar: boolean;  // Show in sidebar menu?
  showInAppBar?: boolean;   // Show in top AppBar?
  children?: NavItem[];  // Optional array for nested items
}

// Define the navigation structure
export const mainNavItems: NavItem[] = [
  // --- Items primarily for MENUS (Sidebar/AppBar) ---
  {
    path: '/',
    label: 'Home',
    icon: 'Home',
    showOnHomepage: false,
    showInSidebar: true,
    showInAppBar: true,
  },
  {
    path: '#', // Non-navigable parent group for menus
    label: 'Modules',
    icon: 'Category',
    showOnHomepage: false,
    showInSidebar: true, // Show group in sidebar
    children: [
      // Actual modules for menus go here
      {
        path: '/info',
        label: 'System Info',
        icon: 'Info',
        showOnHomepage: false, // Not on homepage grid
        showInSidebar: true,   // Appears under 'Modules' in sidebar
        showInAppBar: false,
      },
      {
        path: '/ai-test',
        label: 'AI Test',
        icon: 'Science',
        showOnHomepage: false, // Let's make this NOT show on homepage explicitly for now
                              // We'll use the separate entries below for homepage buttons
        showInSidebar: true,   // Appears under 'Modules' in sidebar
        showInAppBar: false,
      },
      // Add future module links for MENUS here...
    ]
  },
  // Example future "Settings" Group for Menus
  // {
  //   path: '#', label: 'Settings', icon: 'Settings', showInSidebar: true,
  //   children: [ /* ... settings links ... */ ]
  // },


  // --- Items EXPLICITLY for HOMEPAGE BUTTONS ---
  // Set showOnHomepage: true and others false for these
  {
    path: '/ai-test', // Link the AI Test button correctly
    label: 'AI Test',
    icon: 'Science',
    showOnHomepage: true, // YES, show on homepage grid
    showInSidebar: false, // NO, don't show in menus
    showInAppBar: false,  // NO, don't show in menus
  },
  {
    path: '/', // Links home for now, update path when module exists
    label: 'Análise de Documentação para Redação de Quesitos',
    icon: 'Article',
    showOnHomepage: true, showInSidebar: false, showInAppBar: false,
  },
  {
    path: '/', label: 'Pesquisa de Jurisprudências em Direito Previdenciário', icon: 'Balance',
    showOnHomepage: true, showInSidebar: false, showInAppBar: false,
  },
  {
    path: '/', label: 'Análise e Renovação de Documentação Médica', icon: 'Biotech',
    showOnHomepage: true, showInSidebar: false, showInAppBar: false,
  },
  {
    path: '/', label: 'Detectar e Corrigir Inconsistências em Documentos Gerados por I.A.', icon: 'Troubleshoot',
    showOnHomepage: true, showInSidebar: false, showInAppBar: false,
  },
  {
    path: '/', label: 'Gerador de Impugnação de Laudo Pericial', icon: 'Gavel',
    showOnHomepage: true, showInSidebar: false, showInAppBar: false,
  },
  {
    path: '/', label: 'Organizador de Documentos Médicos', icon: 'Folder',
    showOnHomepage: true, showInSidebar: false, showInAppBar: false,
  },
  {
    path: '/', label: 'Analisar e Impugnar Decisão Judicial Previdenciária', icon: 'BalanceScale',
    showOnHomepage: true, showInSidebar: false, showInAppBar: false,
  },
  {
    path: '/', label: 'Construção da Tabela de Evolução da Enfermidade e da Ocupação vs. Limitações', icon: 'TableView',
    showOnHomepage: true, showInSidebar: false, showInAppBar: false,
  },
  // --- END HOMEPAGE BUTTONS ---
];
