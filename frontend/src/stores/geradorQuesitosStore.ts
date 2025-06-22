// frontend/src/stores/geradorQuesitosStore.ts
import { create } from 'zustand';
import {
    RespostaQuesitos,
    // ProcessedDocumentInfo, // No longer directly using this structure from this store's perspective
    uploadDocumentForAnalysis, // Changed from uploadAndProcessPdf
    getTaskStatus,             // New import for polling
    TaskStatusResponse,        // New import
    DocumentUploadResponse,    // New import
    postGerarQuesitosComReferenciaDeDocumento
} from '../services/api';

interface GeradorQuesitosState {
  isLoading: boolean;
  error: string | null;
  quesitosResult: string | null;
  // processedDocumentInfo: ProcessedDocumentInfo | null; // Replaced by taskId and processedFilename
  currentFileBeingProcessed: File | null;
  currentTaskId: string | null; // To store the task ID from uploadDocumentForAnalysis
  processingStatusMessage: string | null; // For UI feedback during polling
  processedFilename: string | null; // Store the filename once processing is successful
  pollingTimerId: NodeJS.Timeout | null; // Store timer ID for polling
}

interface GeradorQuesitosActions {
  fetchQuesitosFromServer: (documentFilename: string, beneficio: string, profissao: string, modelo_nome: string) => Promise<void>; // documentId -> documentFilename
  uploadAndProcessSinglePdfForQuesitos: (file: File, beneficio: string, profissao: string, modelo_nome: string) => Promise<void>;
  clearState: () => void;
  _pollTaskStatus: (taskId: string, originalFilename: string, beneficio: string, profissao: string, modelo_nome: string) => void; // Helper for polling
}

const initialState: GeradorQuesitosState = {
  isLoading: false,
  error: null,
  quesitosResult: null,
  // processedDocumentInfo: null,
  currentFileBeingProcessed: null,
  currentTaskId: null,
  processingStatusMessage: null,
  processedFilename: null,
  pollingTimerId: null,
};

export const useGeradorQuesitosStore = create<GeradorQuesitosState & GeradorQuesitosActions>((set, get) => ({
  ...initialState,

  fetchQuesitosFromServer: async (documentFilename: string, beneficio: string, profissao: string, modelo_nome: string) => {
    set({ isLoading: true, error: null, quesitosResult: null, processingStatusMessage: 'Gerando quesitos...' });
    try {
      const payload = { document_filename: documentFilename, beneficio, profissao, modelo_nome };
      const result: RespostaQuesitos = await postGerarQuesitosComReferenciaDeDocumento(payload);
      set({
        quesitosResult: result.quesitos_texto,
        isLoading: false,
        currentFileBeingProcessed: null,
        processingStatusMessage: 'Quesitos gerados com sucesso!',
        currentTaskId: null, // Clear task ID after final success
      });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Ocorreu um erro desconhecido ao gerar quesitos.';
      set({ error: errorMessage, isLoading: false, currentFileBeingProcessed: null, processingStatusMessage: 'Falha ao gerar quesitos.' });
    }
  },

  _pollTaskStatus: async (taskId: string, originalFilename: string, beneficio: string, profissao: string, modelo_nome: string) => {
    try {
      const statusResponse: TaskStatusResponse = await getTaskStatus(taskId);
      set({ processingStatusMessage: `Status do processamento (${originalFilename}): ${statusResponse.status}` });

      if (statusResponse.status === 'SUCCESS') {
        if (get().pollingTimerId) clearInterval(get().pollingTimerId!);
        set({ pollingTimerId: null, processedFilename: originalFilename, processingStatusMessage: `Processamento de '${originalFilename}' concluído. Gerando quesitos...` });
        // Now that processing is successful, fetch the quesitos
        await get().fetchQuesitosFromServer(originalFilename, beneficio, profissao, modelo_nome);
      } else if (statusResponse.status === 'FAILURE' || statusResponse.status === 'REVOKED') {
        if (get().pollingTimerId) clearInterval(get().pollingTimerId!);
        set({
          pollingTimerId: null,
          error: `Falha no processamento do arquivo '${originalFilename}': ${statusResponse.error_info?.error || 'Erro desconhecido no processamento.'}`,
          isLoading: false,
          currentFileBeingProcessed: null,
          currentTaskId: null,
          processingStatusMessage: `Falha no processamento de '${originalFilename}'.`,
        });
      } else if (statusResponse.status === 'PENDING' || statusResponse.status === 'STARTED' || statusResponse.status === 'RETRY') {
        // Continue polling
        const timerId = setTimeout(() => get()._pollTaskStatus(taskId, originalFilename, beneficio, profissao, modelo_nome), 5000); // Poll every 5 seconds
        set({ pollingTimerId: timerId });
      }
    } catch (pollError) {
      if (get().pollingTimerId) clearInterval(get().pollingTimerId!);
      const errorMessage = pollError instanceof Error ? pollError.message : 'Erro ao verificar status do processamento.';
      set({
        pollingTimerId: null,
        error: errorMessage,
        isLoading: false,
        currentFileBeingProcessed: null,
        currentTaskId: null,
        processingStatusMessage: 'Erro ao verificar status.',
      });
    }
  },

  uploadAndProcessSinglePdfForQuesitos: async (file: File, beneficio: string, profissao: string, modelo_nome: string) => {
    if (get().pollingTimerId) clearInterval(get().pollingTimerId!); // Clear any existing poll timer

    set({
      isLoading: true,
      error: null,
      quesitosResult: null,
      // processedDocumentInfo: null,
      currentFileBeingProcessed: file,
      currentTaskId: null,
      processingStatusMessage: `Enviando '${file.name}' para processamento...`,
      processedFilename: null,
      pollingTimerId: null,
    });

    try {
      const uploadResponse: DocumentUploadResponse = await uploadDocumentForAnalysis(file);
      set({
        currentTaskId: uploadResponse.transcriber_data.task_id,
        processingStatusMessage: `Arquivo '${uploadResponse.original_filename}' enviado. Aguardando processamento (Task ID: ${uploadResponse.transcriber_data.task_id})...`
      });
      // Start polling for status
      get()._pollTaskStatus(uploadResponse.transcriber_data.task_id, uploadResponse.original_filename, beneficio, profissao, modelo_nome);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Ocorreu um erro desconhecido durante o upload do PDF.';
      set({ error: errorMessage, isLoading: false, currentFileBeingProcessed: null, processingStatusMessage: 'Falha no upload.' });
    }
  },

  clearState: () => {
    if (get().pollingTimerId) clearInterval(get().pollingTimerId!);
    set(initialState);
  },

}));