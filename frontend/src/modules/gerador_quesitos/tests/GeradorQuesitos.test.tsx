// frontend/src/modules/gerador_quesitos/tests/GeradorQuesitos.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { vi } from 'vitest';
import GeradorQuesitos from '../GeradorQuesitos';
import { useAuth } from '../../../core_module/auth/hooks/useAuth';
import { useApi } from '../../../core_module/common/hooks/useApi';
import { useNotify } from '../../../core_module/common/hooks/useNotify';

// Mockear os hooks customizados
vi.mock('../../../core_module/auth/hooks/useAuth');
vi.mock('../../../core_module/common/hooks/useApi');
vi.mock('../../../core_module/common/hooks/useNotify');

// Mockear o componente de Notificacao (se ele for renderizado diretamente e interferir)
vi.mock('../../../core_module/common/components/Notificacao', () => ({
  default: ({ message, type, open, onClose }: any) =>
    open && message ? <div data-testid="mock-notification" data-type={type}>{message}</div> : null,
}));


describe('GeradorQuesitos Component', () => {
  const mockLogin = vi.fn();
  const mockLogout = vi.fn();
  const mockGet = vi.fn();
  const mockPost = vi.fn();
  const mockNotify = vi.fn();

  beforeEach(() => {
    (useAuth as any).mockReturnValue({
      user: { token: 'fake-token' },
      login: mockLogin,
      logout: mockLogout,
      isAuthenticated: true,
    });
    (useApi as any).mockReturnValue({
      get: mockGet,
      post: mockPost,
      loading: false,
    });
    (useNotify as any).mockReturnValue(mockNotify);

    // Reset mocks
    mockPost.mockReset();
    mockNotify.mockReset();
    mockGet.mockReset();
  });

  test('GQ-FE-001 (parcial): renders and allows PDF upload and theme input', async () => {
    mockPost
      .mockResolvedValueOnce({ data: { document_id: 'doc123', message: 'Documento processado' } }) // Simula upload
      .mockResolvedValueOnce({ data: { quesitos: ['Quesito 1?', 'Quesito 2?'] } }); // Simula geração de quesitos

    render(<GeradorQuesitos />);

    // Verifica se o título está presente
    expect(screen.getByText('Gerador de Quesitos (Refatorado)')).toBeInTheDocument();

    // Simula seleção de arquivo
    const fileInput = screen.getByLabelText(/selecionar arquivo pdf/i);
    const fakeFile = new File(['dummy content'], 'test.pdf', { type: 'application/pdf' });
    fireEvent.change(fileInput, { target: { files: [fakeFile] } });

    // Verifica se o nome do arquivo é exibido (se houver essa funcionalidade)
    // Se não, apenas verifica se o input tem o arquivo.
    // Exemplo: expect(screen.getByText('test.pdf')).toBeInTheDocument();

    // Insere o tema
    const themeInput = screen.getByLabelText(/tema\/contexto para os quesitos/i);
    fireEvent.change(themeInput, { target: { value: 'Direito Civil' } });
    expect(themeInput).toHaveValue('Direito Civil');

    // Clica em gerar quesitos
    const submitButton = screen.getByRole('button', { name: /gerar quesitos/i });
    fireEvent.click(submitButton);

    // Verifica se a API de upload foi chamada
    await waitFor(() => {
      expect(mockPost).toHaveBeenCalledWith(
        '/documents/upload-and-process',
        expect.any(FormData), // FormData é usado para upload de arquivos
        { headers: { Authorization: 'Bearer fake-token', 'Content-Type': 'multipart/form-data' } }
      );
    });

    // Verifica se a notificação de processamento foi chamada (se aplicável)
    // await waitFor(() => {
    //   expect(mockNotify).toHaveBeenCalledWith('Documento enviado para processamento...', 'info');
    // });

    // Verifica se a API de geração de quesitos foi chamada após o upload
    await waitFor(() => {
      expect(mockPost).toHaveBeenCalledWith(
        '/gerador_quesitos/gerar_refatorado',
        { document_id: 'doc123', tema: 'Direito Civil' },
        { headers: { Authorization: 'Bearer fake-token' } }
      );
    });

    // Verifica se os quesitos são exibidos
    await waitFor(() => {
      expect(screen.getByText('Quesito 1?')).toBeInTheDocument();
      expect(screen.getByText('Quesito 2?')).toBeInTheDocument();
    });
     // Verifica a notificação de sucesso
     await waitFor(() => {
        expect(mockNotify).toHaveBeenCalledWith('Quesitos gerados com sucesso!', 'success');
      });
  });

  test('GQ-FE-002: shows error for invalid file type', async () => {
    render(<GeradorQuesitos />);

    const fileInput = screen.getByLabelText(/selecionar arquivo pdf/i);
    const invalidFile = new File(['dummy content'], 'test.txt', { type: 'text/plain' });
    fireEvent.change(fileInput, { target: { files: [invalidFile] } });

    // Clica em gerar quesitos
    const submitButton = screen.getByRole('button', { name: /gerar quesitos/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
        expect(mockNotify).toHaveBeenCalledWith('Por favor, selecione um arquivo PDF.', 'error');
    });
    expect(mockPost).not.toHaveBeenCalled();
  });

  test('GQ-FE-003: shows error on PDF upload failure', async () => {
    mockPost.mockRejectedValueOnce(new Error('Upload failed'));
    render(<GeradorQuesitos />);

    const fileInput = screen.getByLabelText(/selecionar arquivo pdf/i);
    const fakeFile = new File(['dummy content'], 'test.pdf', { type: 'application/pdf' });
    fireEvent.change(fileInput, { target: { files: [fakeFile] } });

    const themeInput = screen.getByLabelText(/tema\/contexto para os quesitos/i);
    fireEvent.change(themeInput, { target: { value: 'Direito Penal' } });

    const submitButton = screen.getByRole('button', { name: /gerar quesitos/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockPost).toHaveBeenCalledWith(
        '/documents/upload-and-process',
        expect.any(FormData),
        expect.anything()
      );
    });

    await waitFor(() => {
      expect(mockNotify).toHaveBeenCalledWith('Falha ao processar o documento. Error: Upload failed', 'error');
    });
  });

  test('GQ-FE-004: shows error on quesitos generation failure', async () => {
    mockPost
      .mockResolvedValueOnce({ data: { document_id: 'doc456', message: 'Documento processado' } }) // Upload OK
      .mockRejectedValueOnce(new Error('Generation failed')); // Geração de quesitos falha

    render(<GeradorQuesitos />);

    const fileInput = screen.getByLabelText(/selecionar arquivo pdf/i);
    const fakeFile = new File(['dummy content'], 'test.pdf', { type: 'application/pdf' });
    fireEvent.change(fileInput, { target: { files: [fakeFile] } });

    const themeInput = screen.getByLabelText(/tema\/contexto para os quesitos/i);
    fireEvent.change(themeInput, { target: { value: 'Direito Tributário' } });

    const submitButton = screen.getByRole('button', { name: /gerar quesitos/i });
    fireEvent.click(submitButton);

    // Espera a primeira chamada (upload)
    await waitFor(() => {
      expect(mockPost).toHaveBeenCalledWith('/documents/upload-and-process', expect.any(FormData), expect.anything());
    });

    // Espera a segunda chamada (geração de quesitos)
    await waitFor(() => {
      expect(mockPost).toHaveBeenCalledWith('/gerador_quesitos/gerar_refatorado',
        { document_id: 'doc456', tema: 'Direito Tributário' },
        expect.anything()
      );
    });

    await waitFor(() => {
      expect(mockNotify).toHaveBeenCalledWith('Falha ao gerar quesitos. Error: Generation failed', 'error');
    });
  });

  test('GQ-FE-005: shows loading state', async () => {
    // Configura o mockPost para ter um atraso e depois resolver
    (useApi as any).mockReturnValue({
        get: mockGet,
        post: vi.fn(async () => {
          // Simula um atraso na API
          await new Promise(resolve => setTimeout(resolve, 100));
          // Decide o que retornar baseado no número de chamadas
          if (mockPost.mock.calls.length <= 1) { // Primeira chamada (upload)
            return { data: { document_id: 'doc789', message: 'Documento processado' } };
          } else { // Segunda chamada (gerar quesitos)
            return { data: { quesitos: ['Quesito de Teste?'] } };
          }
        }),
        loading: true, // Simula o estado de loading do hook useApi
      });

      render(<GeradorQuesitos />);

      // Verifica se o botão de submit está desabilitado e com texto de "Carregando..."
      // Isso depende da implementação do componente GeradorQuesitos
      // Por exemplo, se o botão muda de texto ou fica desabilitado:
      // expect(screen.getByRole('button', { name: /carregando/i })).toBeDisabled();
      // Ou se um spinner é exibido:
      // expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();

      // Para este teste, vamos verificar se o botão fica desabilitado enquanto 'loading' é true
      // A lógica exata de desabilitar o botão durante o loading precisa estar no GeradorQuesitos.tsx

      const submitButton = screen.getByRole('button', { name: /gerar quesitos/i });
      expect(submitButton).toBeDisabled(); // Assumindo que o botão é desabilitado quando loading=true
      // E/OU que o texto do botão muda
      // expect(screen.getByRole('button', { name: /processando.../i })).toBeInTheDocument();


      // Para simular o fluxo completo e verificar os estados de loading intermediários:
      // Restaurar o mock do useApi para não ser mais loading=true após a ação inicial
      (useApi as any).mockReturnValue({
        get: mockGet,
        post: mockPost, // usa o mockPost original com as resoluções configuradas no beforeEach
        loading: false,
      });
      mockPost
        .mockImplementationOnce(async () => { // Upload
            (useApi as any).setState({ loading: true }); // Simula loading=true durante esta chamada
            await new Promise(resolve => setTimeout(resolve, 50));
            (useApi as any).setState({ loading: false });
            return { data: { document_id: 'doc789', message: 'Documento processado' }};
        })
        .mockImplementationOnce(async () => { // Geração
            (useApi as any).setState({ loading: true });
            await new Promise(resolve => setTimeout(resolve, 50));
            (useApi as any).setState({ loading: false });
            return { data: { quesitos: ['Quesito de Teste?'] }};
        });


    // Re-renderiza ou dispara a ação que ativa o loading
    const fileInput = screen.getByLabelText(/selecionar arquivo pdf/i);
    const fakeFile = new File(['dummy content'], 'test.pdf', { type: 'application/pdf' });
    fireEvent.change(fileInput, { target: { files: [fakeFile] } });

    const themeInput = screen.getByLabelText(/tema\/contexto para os quesitos/i);
    fireEvent.change(themeInput, { target: { value: 'Tema Teste Loading' } });

    // O botão deve estar habilitado antes do clique
    expect(submitButton).not.toBeDisabled();

    // Clica no botão
    fireEvent.click(submitButton);

    // Durante a primeira chamada (upload), o botão deveria estar desabilitado
    // Esta verificação é difícil de fazer precisamente sem controlar o estado de `loading` dentro do componente.
    // A melhor abordagem seria o componente GeradorQuesitos usar o `loading` de `useApi` para desabilitar o botão.
    // E o mock de `useApi` ser atualizado para refletir `loading: true` durante as chamadas mockadas.

    // Exemplo de como poderia ser se o botão mudasse o texto:
    // await waitFor(() => expect(screen.getByRole('button', { name: /processando upload.../i })).toBeInTheDocument());

    // Após a primeira chamada, e antes da segunda
    // await waitFor(() => expect(screen.getByRole('button', { name: /gerando quesitos.../i })).toBeInTheDocument());

    // Checagem final
    await waitFor(() => {
        expect(screen.getByText('Quesito de Teste?')).toBeInTheDocument();
      });
    expect(submitButton).not.toBeDisabled(); // Botão habilitado novamente
  });

  test('GQ-FE-006: allows clearing selected file and results', async () => {
    mockPost
      .mockResolvedValueOnce({ data: { document_id: 'doc123', message: 'Documento processado' } })
      .mockResolvedValueOnce({ data: { quesitos: ['Quesito Limpeza?'] } });

    render(<GeradorQuesitos />);

    // Selecionar arquivo
    const fileInput = screen.getByLabelText(/selecionar arquivo pdf/i) as HTMLInputElement;
    const fakeFile = new File(['dummy content'], 'test.pdf', { type: 'application/pdf' });
    fireEvent.change(fileInput, { target: { files: [fakeFile] } });

    // Verificar se o nome do arquivo é exibido (ou se o input tem valor)
    // Esta parte depende de como o componente exibe o arquivo selecionado
    // Supondo que o nome do arquivo é mostrado:
    // await waitFor(() => expect(screen.getByText('test.pdf')).toBeInTheDocument());
    // Ou, se não há exibição direta, o input.files deve ter o arquivo
    expect(fileInput.files?.[0]).toBe(fakeFile);
    expect(fileInput.files?.length).toBe(1);

    // Insere tema e gera quesitos
    const themeInput = screen.getByLabelText(/tema\/contexto para os quesitos/i);
    fireEvent.change(themeInput, { target: { value: 'Tema Limpeza' } });
    fireEvent.click(screen.getByRole('button', { name: /gerar quesitos/i }));

    await waitFor(() => expect(screen.getByText('Quesito Limpeza?')).toBeInTheDocument());

    // Clicar no botão "Limpar" (ou "Nova Consulta")
    // O nome/texto exato do botão depende da sua implementação no GeradorQuesitos.tsx
    const clearButton = screen.getByRole('button', { name: /nova consulta/i });
    fireEvent.click(clearButton);

    // Verificar se o arquivo foi limpo (input de arquivo está vazio)
    expect(fileInput.files?.length).toBe(0);
    // Verificar se o tema foi limpo
    expect(themeInput).toHaveValue('');
    // Verificar se os quesitos foram limpos da tela
    expect(screen.queryByText('Quesito Limpeza?')).not.toBeInTheDocument();
    // Verificar se a lista de quesitos está vazia (se a lista é sempre renderizada)
    const quesitosList = screen.queryByRole('list', {name: /lista de quesitos/i }); // Supondo que a lista tem um aria-label
    if (quesitosList) {
      expect(quesitosList.children.length).toBe(0);
    }
  });

});

// Adicionar um mock simples para setState no useApi se ele for usado para controlar o estado de loading internamente
// Isso é uma simplificação. Em um cenário real, o hook useApi gerenciaria seu próprio estado.
(useApi as any).setState = (newState: any) => {
    (useApi as any).mockReturnValue({
        ...(useApi as any)(), // Preserva os mocks de get/post
        ...newState, // Sobrescreve com o novo estado (ex: loading)
    });
};
