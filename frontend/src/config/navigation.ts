// frontend/src/config/navigation.ts

export interface NavItem {
  path: string;
  label: string;
  icon: string;
  showOnHomepage?: boolean;
  showInSidebar: boolean;
  showInAppBar?: boolean;
  children?: NavItem[];
}

export const mainNavItems: NavItem[] = [
  // --- Items for Menus/Routing ---
  {
    path: '/',
    label: 'Home',
    icon: 'Home',
    showOnHomepage: false,
    showInSidebar: true, // Keep in Sidebar
    showInAppBar: false, // Hide from AppBar
  },
  {
    path: '/info',
    label: 'System Info',
    icon: 'Info',
    showOnHomepage: false,
    showInSidebar: false, // Hide from Sidebar
    showInAppBar: true,   // Show ONLY in AppBar
  },
  {
    path: '#', // Modules Group Header (for Sidebar)
    label: 'Modules',
    icon: 'Category',
    showOnHomepage: false,
    showInSidebar: true, // Show group header in sidebar
    children: [
      {
        path: '/gerador-quesitos',
        label: 'Gerador Quesitos',
        icon: 'Quiz',
        showOnHomepage: false, // Will be shown via separate entry below
        showInSidebar: true,   // Show under Modules in sidebar
        showInAppBar: false,
      },
      // Add future modules for sidebar menu here...
    ]
  },
  { // AI Test - Hidden completely
    path: '/ai-test',
    label: 'AI Test',
    icon: 'Science',
    showOnHomepage: false,
    showInSidebar: false,
    showInAppBar: false,
  },

  // --- Items EXPLICITLY for HOMEPAGE BUTTONS ---
  {
    path: '/gerador-quesitos', // Link to the actual module page
    label: 'Gerador de Quesitos', // Label for homepage button
    icon: 'Quiz',
    showOnHomepage: true, // YES, show on homepage grid
    showInSidebar: false, // NO, don't show in menus (already in group above)
    showInAppBar: false,
  },
  // --- Restored 8 Placeholders for Homepage ---
  {
    path: '/', // Link home for now
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
