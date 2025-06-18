import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { getDocumentProcessingStatus, TaskStatusResponse } from '../../../services/api'; // Adjust path

export type ProcessingStatus = 'idle' | 'uploading' | 'processing' | 'success' | 'error' | 'queued';

interface AnalisadorState {
  currentTaskId: string | null;
  status: ProcessingStatus;
  progress: number; // 0-100, or -1 for indeterminate
  statusMessage: string | null;
  errorMessage: string | null;
  processedDocumentId: string | null; // e.g., filename or DB ID from task result on success
  pollingTimerId: any | null; // Using 'any' for simplicity with setTimeout ID
}

interface AnalisadorActions {
  resetState: () => void;
  setUploading: () => void;
  setUploadSuccess: (taskId: string, initialMessage?: string) => void;
  _pollStatus: () => Promise<void>; // Internal polling action
  stopPolling: () => void;
}

const initialState: AnalisadorState = {
  currentTaskId: null,
  status: 'idle',
  progress: 0,
  statusMessage: null,
  errorMessage: null,
  processedDocumentId: null,
  pollingTimerId: null,
};

export const useAnalisadorStore = create<AnalisadorState & AnalisadorActions>()(
  devtools(
    (set, get) => ({
      ...initialState,
      resetState: () => {
        get().stopPolling();
        set(initialState);
      },
      setUploading: () => set({
        status: 'uploading',
        errorMessage: null,
        statusMessage: 'Enviando arquivo...',
        progress: 0, // Or a small value like 5 to show something started
        currentTaskId: null,
        processedDocumentId: null,
      }),
      setUploadSuccess: (taskId, initialMessage) => {
        get().stopPolling(); // Stop any previous polling
        set({
          currentTaskId: taskId,
          status: 'queued', // Or 'processing' if backend immediately starts
          statusMessage: initialMessage || 'Arquivo na fila para processamento...',
          errorMessage: null,
          progress: 0, // Or an initial progress if known
          processedDocumentId: null,
        });
        // Clear previous timer before starting a new one
        if (get().pollingTimerId) {
            clearTimeout(get().pollingTimerId!);
        }
        const newTimerId = setTimeout(get()._pollStatus, 100); // Start polling almost immediately
        set({ pollingTimerId: newTimerId });
      },
      stopPolling: () => {
        const timerId = get().pollingTimerId;
        if (timerId) {
          clearTimeout(timerId);
          set({ pollingTimerId: null });
        }
      },
      _pollStatus: async () => {
        const taskId = get().currentTaskId;
        if (!taskId) {
          get().stopPolling();
          return;
        }

        try {
          const response = await getDocumentProcessingStatus(taskId);
          let newStatus: ProcessingStatus = get().status;
          let newProgress = get().progress;
          let newStatusMessage = get().statusMessage;
          let newErrorMessage = null;
          let newProcessedDocumentId = get().processedDocumentId;

          switch (response.status.toUpperCase()) {
            case 'PENDING':
            case 'QUEUED':
              newStatus = 'queued';
              newStatusMessage = response.result?.message || 'Na fila para processamento...';
              // Example: if result is an object with progress
              newProgress = typeof response.result?.progress === 'number' ? response.result.progress : 10;
              break;
            case 'STARTED':
            case 'PROCESSING':
              newStatus = 'processing';
              newStatusMessage = response.result?.message || 'Processando documento...';
              newProgress = typeof response.result?.progress === 'number' ? response.result.progress :
                            (typeof response.result?.current === 'number' ? response.result.current : 30);
              break;
            case 'SUCCESS':
              newStatus = 'success';
              newStatusMessage = response.result?.message || 'Processamento concluído com sucesso!';
              newProgress = 100;
              newProcessedDocumentId = response.result?.document_id || response.result?.filename || taskId;
              break;
            case 'FAILURE':
            case 'FAILED':
              newStatus = 'error';
              newErrorMessage = response.error_info?.error || response.result?.error || 'Falha no processamento.';
              newStatusMessage = null; // Clear status message on error
              newProgress = 0;
              break;
            case 'RETRY':
              newStatus = 'processing'; // Or a specific 'retrying' status
              newStatusMessage = response.result?.message || 'Tentando processar novamente...';
              newProgress = get().progress; // Keep current progress or adjust
              break;
            default:
              console.warn('Unknown task status from backend:', response.status);
              newStatusMessage = `Status desconhecido: ${response.status}`;
              // Potentially keep polling or set to error based on desired behavior
          }

          set({
            status: newStatus,
            progress: newProgress,
            statusMessage: newStatusMessage,
            errorMessage: newErrorMessage,
            processedDocumentId: newProcessedDocumentId,
            pollingTimerId: null // Clear current timer ID before potentially setting a new one
          });

          if (newStatus === 'processing' || newStatus === 'queued' || (newStatus === 'processing' && response.status.toUpperCase() === 'RETRY')) {
            const newTimerId = setTimeout(get()._pollStatus, 3000); // Poll every 3 seconds
            set({ pollingTimerId: newTimerId });
          } else {
            get().stopPolling(); // Stop polling on final states (success, error) or unknown
          }

        } catch (error: any) {
          console.error('Polling API error:', error);
          // If API call itself fails (e.g. network error, 50x from gateway status endpoint)
          set({
            status: 'error',
            errorMessage: error.message || 'Erro ao buscar status da tarefa.',
            pollingTimerId: null // Stop polling on error
          });
          get().stopPolling();
        }
      },
    }),
    { name: 'analisador-documentos-store' }
  )
);
