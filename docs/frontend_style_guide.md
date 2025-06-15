# Guia de Estilo do Frontend - Modular Dashboard

## Introdução

Este guia de estilo documenta os padrões visuais e de componentes para o frontend do projeto Modular Dashboard. O objetivo é garantir consistência visual, melhorar a usabilidade e acelerar o desenvolvimento através da reutilização de componentes e diretrizes claras.

A interface do Modular Dashboard é construída sobre [Material UI (MUI)](https://mui.com/). Este guia detalha como utilizamos e estendemos os componentes do MUI para atender às necessidades específicas do nosso projeto. Todos os componentes e exemplos devem seguir o idioma pt-BR.

## Sumário
* [Tipografia](#tipografia)
* [Cores](#cores) (Observação: Este guia foca em componentes, mas uma breve menção às cores primárias/secundárias pode ser útil)
* [Botões](#botoes)
* [Inputs de Formulário](#inputs-de-formulario)
* [Cards](#cards)
* [Modais](#modais)
* [Componentes Comuns Reutilizáveis](#componentes-comuns-reutilizaveis)
* [Notas de Customização MUI](#notas-de-customizacao-mui)

---

## Tipografia

A tipografia é gerenciada pelo componente `<Typography>` do MUI. Para manter a consistência, utilize as seguintes variantes de forma padronizada:

*   **Títulos de Página Principal:** `variant="h4"` ou `variant="h5"`. Ex: `<Typography variant="h4" component="h1" gutterBottom>Título da Página</Typography>`
*   **Títulos de Seção Principal:** `variant="h5"` ou `variant="h6"`. Ex: `<Typography variant="h5" component="h2" gutterBottom>Título da Seção</Typography>`
*   **Subtítulos de Seção:** `variant="subtitle1"` ou `variant="subtitle2"`.
*   **Corpo de Texto Principal:** `variant="body1"`.
*   **Texto Secundário ou Menos Enfatizado:** `variant="body2"`.
*   **Legendas e Textos Pequenos:** `variant="caption"`.

Utilize o prop `gutterBottom` quando um espaçamento inferior for apropriado. Para links, considere usar o componente `<Link>` do MUI, que herda estilos de tipografia.

---

## Cores

As cores da aplicação são definidas no arquivo de tema `frontend/src/styles/theme.ts` e seguem a paleta do Material UI.

*   **Primária (`theme.palette.primary.main`):** Usada para ações principais, botões de destaque e elementos de navegação ativos. (Cor atual: Azul)
*   **Secundária (`theme.palette.secondary.main`):** Usada para elementos de menor destaque ou complementares. (Cor atual: Verde)
*   **Erro (`theme.palette.error.main`):** Para mensagens de erro, alertas de falha e ícones de validação negativa. (Cor atual: Vermelho)
*   **Aviso (`theme.palette.warning.main`):** Para alertas e notificações que requerem atenção. (Cor atual: Laranja)
*   **Informação (`theme.palette.info.main`):** Para mensagens informativas e dicas. (Cor atual: Azul claro)
*   **Sucesso (`theme.palette.success.main`):** Para feedback de sucesso e validação positiva. (Cor atual: Verde escuro)

Consulte o `theme.ts` para os valores hexadecimais exatos e para cores de texto (ex: `theme.palette.text.primary`, `theme.palette.text.secondary`).

---

## Botões

Utilize o componente `<Button>` do MUI para todas as ações clicáveis que não sejam links de navegação. Para consistência, utilize preferencialmente o componente `StyledButton` de `frontend/src/components/common/StyledButton.tsx`. Ele é um wrapper direto do `<Button>` do MUI e deve ser usado conforme as diretrizes de variantes e cores mencionadas abaixo.

*   **Variantes:**
    *   `variant="contained"`: Para ações primárias e de maior destaque (ex: "Salvar", "Enviar").
        ```tsx
        // import StyledButton from 'frontend/src/components/common/StyledButton';
        <StyledButton variant="contained" color="primary">Ação Principal</StyledButton>
        ```
    *   `variant="outlined"`: Para ações secundárias (ex: "Cancelar", "Voltar").
        ```tsx
        <StyledButton variant="outlined" color="primary">Ação Secundária</StyledButton>
        ```
    *   `variant="text"`: Para ações de baixa proeminência, como em rodapés de modais ou cards (ex: "Saiba mais").
        ```tsx
        <StyledButton variant="text">Menor Destaque</StyledButton>
        ```
*   **Cores:**
    *   `color="primary"`: Padrão para a maioria das ações.
    *   `color="secondary"`: Para ações alternativas ou menos comuns.
    *   `color="error"`: Para ações destrutivas (ex: "Excluir").
*   **Tamanhos:**
    *   `size="medium"`: Padrão para a maioria dos casos.
    *   `size="small"`: Para contextos onde o espaço é limitado.
    *   `size="large"`: Para botões de call-to-action que precisam de mais destaque.
*   **Estado Desabilitado:**
    *   Utilize o prop `disabled` para indicar que um botão não está acionável.
        ```tsx
        <StyledButton variant="contained" disabled>Ação Desabilitada</StyledButton>
        ```
*   **Ícones:** Botões podem incluir ícones usando `startIcon` ou `endIcon`.
    ```tsx
    // import SaveIcon from '@mui/icons-material/Save';
    // import StyledButton from 'frontend/src/components/common/StyledButton';
    <StyledButton variant="contained" startIcon={<SaveIcon />}>Salvar</StyledButton>
    ```

---

## Inputs de Formulário

Para campos de entrada em formulários, utilize os componentes do MUI como `<TextField>`, `<Select>`, `<Checkbox>`, etc.

*   **Padrão:** `variant="outlined"` para todos os inputs para manter a consistência visual.
*   **Largura:** `fullWidth` deve ser usado na maioria dos casos para que os campos ocupem o espaço disponível no formulário, facilitando o layout.
    ```tsx
    <TextField label="Nome Completo" variant="outlined" fullWidth />
    ```
*   **Labels:** Todas as labels devem ser claras, concisas e em pt-BR. Utilize o prop `label` nos componentes.
*   **`<Select>`:**
    ```tsx
    <FormControl fullWidth variant="outlined">
      <InputLabel id="select-label-id">Categoria</InputLabel>
      <Select labelId="select-label-id" label="Categoria">
        <MenuItem value="opcao1">Opção 1</MenuItem>
        <MenuItem value="opcao2">Opção 2</MenuItem>
      </Select>
    </FormControl>
    ```
*   **Validação e Erros:** Utilize o prop `error` e `helperText` para exibir feedback de validação.
    ```tsx
    <TextField label="Email" variant="outlined" fullWidth error={!!emailError} helperText={emailError} />
    ```

---

## Cards

O componente `<Card>` do MUI é utilizado para agrupar informações relacionadas em um contêiner visualmente distinto. Para cards de informação padronizados, utilize o componente `InfoCard` de `frontend/src/components/common/InfoCard.tsx`.

*   **`InfoCard` Props Principais:**
    *   `title: ReactNode`: Título do card, exibido no `CardHeader`.
    *   `subheader?: ReactNode`: Subtítulo do card, exibido no `CardHeader`.
    *   `children: ReactNode`: Conteúdo principal do card, inserido em `<CardContent>`.
    *   `cardActions?: ReactNode`: Permite adicionar uma seção de ações (`<CardActions>`) ao final do card.
    *   `action?: ReactNode`: Elemento de ação para o `CardHeader` (ex: um `IconButton`).
*   **Exemplo com `InfoCard`:**
    ```tsx
    // import InfoCard from 'frontend/src/components/common/InfoCard';
    // import { Button } from '@mui/material'; // ou StyledButton
    <InfoCard
      title="Título do Card de Informação"
      subheader="Subtítulo se necessário"
      cardActions={<Button size="small">Saiba Mais</Button>}
    >
      <Typography variant="body2">
        Este é o conteúdo principal do InfoCard. Ele pode conter qualquer elemento React.
      </Typography>
    </InfoCard>
    ```
*   **Estrutura Básica (usando MUI diretamente):**
    *   `<CardHeader>`: Para títulos (prop `title`) e subtítulos (prop `subheader`).
    *   `<CardContent>`: Para o corpo principal do card.
    *   `<CardActions>`: Para botões de ação.
*   **Elevação:** A elevação padrão (`elevation={1}`) é geralmente suficiente. Aumente (`elevation={3}` ou mais) para dar mais destaque se necessário, mas use com moderação.

---

## Modais

Modais (ou caixas de diálogo) são utilizados para interações que exigem foco total do usuário. Para modais padronizados, utilize o componente `StandardModal` de `frontend/src/components/common/StandardModal.tsx`.

*   **`StandardModal` Props Principais:**
    *   `title: ReactNode`: Título do modal.
    *   `children: ReactNode`: Conteúdo principal do modal, inserido em `<DialogContent>`.
    *   `actions?: ReactNode`: Conteúdo para a seção de ações (`<DialogActions>`), tipicamente botões.
    *   `open: boolean`: Controla a visibilidade do modal.
    *   `onClose: () => void`: Função chamada quando o modal solicita fechamento (ex: clique no backdrop ou no botão de fechar).
    *   `showCloseButton?: boolean`: Exibe um botão 'X' no canto superior direito (padrão: `true`).
*   **Exemplo com `StandardModal`:**
    ```tsx
    // import StandardModal from 'frontend/src/components/common/StandardModal';
    // import { Button } from '@mui/material'; // ou StyledButton
    // No seu componente React:
    // const [isModalOpen, setIsModalOpen] = useState(false);
    //
    // <Button onClick={() => setIsModalOpen(true)}>Abrir Modal</Button>
    // <StandardModal
    //   title="Título do Modal Padrão"
    //   open={isModalOpen}
    //   onClose={() => setIsModalOpen(false)}
    //   actions={
    //     <>
    //       <Button onClick={() => setIsModalOpen(false)}>Cancelar</Button>
    //       <Button onClick={() => { /* Ação de confirmação */ setIsModalOpen(false); }} color="primary">
    //         Confirmar
    //       </Button>
    //     </>
    //   }
    // >
    //   <Typography variant="body1">
    //     Este é o conteúdo principal do StandardModal.
    //   </Typography>
    // </StandardModal>
    ```
*   **Estrutura Padrão (usando MUI diretamente):**
    *   `<DialogTitle>`, `<DialogContent>`, `<DialogActions>`.
*   **Responsividade:** Modais do MUI são responsivos. `StandardModal` também herda essa característica. Considere o prop `fullScreen` para modais que devem ocupar a tela inteira em dispositivos móveis.

---

## Componentes Comuns Reutilizáveis

Esta seção lista os componentes React reutilizáveis criados para manter a consistência e acelerar o desenvolvimento.

### 1. `StyledButton`
- **Localização:** `frontend/src/components/common/StyledButton.tsx`
- **Descrição:** Wrapper padrão para o componente `<Button>` do Material UI. Garante o uso consistente de botões em toda a aplicação, seguindo as diretrizes de variantes, cores e tamanhos.
- **Detalhes:** Veja a seção [Botões](#botoes).

### 2. `InfoCard`
- **Localização:** `frontend/src/components/common/InfoCard.tsx`
- **Descrição:** Componente padronizado para exibir informações em formato de card. Oferece uma estrutura consistente com `CardHeader`, `CardContent` e `CardActions` opcionais.
- **Props Principais:** `title`, `subheader`, `children` (conteúdo), `cardActions`, `action` (para header).
- **Detalhes:** Veja a seção [Cards](#cards).

### 3. `StandardModal`
- **Localização:** `frontend/src/components/common/StandardModal.tsx`
- **Descrição:** Componente padronizado para diálogos modais. Inclui `DialogTitle` com um botão de fechar opcional, `DialogContent` com divisórias, e `DialogActions`.
- **Props Principais:** `title`, `children` (conteúdo), `actions`, `open`, `onClose`, `showCloseButton`.
- **Detalhes:** Veja a seção [Modais](#modais).

---

## Notas de Customização MUI

A customização de componentes MUI no projeto deve seguir as seguintes abordagens, em ordem de preferência:

1.  **Prop `sx`:** Para ajustes de estilo pontuais e específicos de uma instância do componente. É ideal para overrides rápidos sem a necessidade de criar um novo componente.
    ```tsx
    <Button sx={{ mt: 2, backgroundColor: 'customColor.main' }}>Botão Customizado</Button>
    ```
2.  **Utilitário `styled()`:** Para criar novos componentes reutilizáveis que encapsulam estilos mais complexos ou variantes de design de um componente MUI base. Estes devem ser usados quando um padrão de customização se repete.
    ```tsx
    const StyledCustomCard = styled(Card)(({ theme }) => ({
      marginBottom: theme.spacing(3),
      // ... outros estilos
    }));
    ```
3.  **Overrides Globais no Tema (`frontend/src/styles/theme.ts`):** Para modificações que devem afetar todas as instâncias de um componente MUI na aplicação (ex: mudar a elevação padrão de todos os `Card`s). Use com moderação para evitar complexidade excessiva no tema.
    ```typescript
    // Dentro de createTheme, na seção components:
    MuiButton: {
      styleOverrides: {
        root: { // Estilo para todos os botões
          textTransform: 'none', // Ex: desabilitar uppercase padrão
        }
      }
    }
    ```

Priorize o uso do `sx` para simplicidade e `styled()` para reutilização. Modificações globais no tema devem ser bem justificadas e discutidas.
