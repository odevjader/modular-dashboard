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

// Define the navigation structure
export const mainNavItems: NavItem[] = [
  // --- Items for Menus/Routing ---
  { // Home: Only in Sidebar
    path: '/',
    label: 'Home',
    icon: 'Home',
    showOnHomepage: false,
    showInSidebar: true,
    showInAppBar: false,
  },
  { // System Info: Only in AppBar
    path: '/info',
    label: 'System Info',
    icon: 'Info',
    showOnHomepage: false,
    showInSidebar: false,
    showInAppBar: true,
  },
  { // Modules Group Header (for Sidebar)
    path: '#',
    label: 'Modules',
    icon: 'Category',
    showOnHomepage: false,
    showInSidebar: true,
    children: [
      { // Gerador Quesitos: Only under Modules in Sidebar menu
        path: '/gerador-quesitos',
        label: 'Gerador Quesitos',
        icon: 'Quiz', // Using Quiz icon
        showOnHomepage: false, // Homepage button is defined separately below
        showInSidebar: true,
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
  { // Gerador Quesitos: Button on Homepage
    path: '/gerador-quesitos',
    label: 'Gerador de Quesitos', // Label for homepage button
    icon: 'Quiz', // Use same icon identifier
    showOnHomepage: true,
    showInSidebar: false, // Not duplicated in root of sidebar
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
