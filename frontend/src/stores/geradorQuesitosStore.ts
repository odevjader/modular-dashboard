// frontend/src/stores/geradorQuesitosStore.ts
import { create } from 'zustand';
import {
    RespostaQuesitos,
    ProcessedDocumentInfo, // New import
    uploadAndProcessPdf,      // New import for the gateway call
    postGerarQuesitosComReferenciaDeDocumento // New import for the refactored quesitos generation
} from '../services/api';

interface GeradorQuesitosState {
  isLoading: boolean;
  error: string | null;
  quesitosResult: string | null;
  processedDocumentInfo: ProcessedDocumentInfo | null; // New state field
  currentFileBeingProcessed: File | null; // New state field to track the file
}

interface GeradorQuesitosActions {
  // Renamed and signature changed
  fetchQuesitosFromServer: (documentId: number, beneficio: string, profissao: string, modelo_nome: string) => Promise<void>;
  // New action
  uploadAndProcessSinglePdfForQuesitos: (file: File, beneficio: string, profissao: string, modelo_nome: string) => Promise<void>;
  clearState: () => void;
}

const initialState: GeradorQuesitosState = {
  isLoading: false,
  error: null,
  quesitosResult: null,
  processedDocumentInfo: null, // Initialize new field
  currentFileBeingProcessed: null, // Initialize new field
};

export const useGeradorQuesitosStore = create<GeradorQuesitosState & GeradorQuesitosActions>((set, get) => ({
  ...initialState,

  // Renamed from generateQuesitos, new signature, new API call
  fetchQuesitosFromServer: async (documentId: number, beneficio: string, profissao: string, modelo_nome: string) => {
    console.log('[Store Action] fetchQuesitosFromServer: Iniciando...');
    // isLoading is already true if called from uploadAndProcessSinglePdfForQuesitos
    // If called directly, ensure isLoading is set:
    if (!get().isLoading) {
        set({ isLoading: true, error: null, quesitosResult: null });
    } else {
        set({ error: null, quesitosResult: null }); // Clear previous results/errors but keep loading
    }
    console.log('[Store Action] fetchQuesitosFromServer: isLoading potentially set');

    try {
      console.log('[Store Action] fetchQuesitosFromServer: Chamando postGerarQuesitosComReferenciaDeDocumento API...');
      const payload = { document_id: documentId, beneficio, profissao, modelo_nome };
      const result: RespostaQuesitos = await postGerarQuesitosComReferenciaDeDocumento(payload);
      console.log('[Store Action] fetchQuesitosFromServer: API Sucesso!', result);
      set({ quesitosResult: result.quesitos_texto, isLoading: false, currentFileBeingProcessed: null });
      console.log('[Store Action] fetchQuesitosFromServer: State atualizado com sucesso, isLoading false');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Ocorreu um erro desconhecido ao gerar quesitos.';
      console.error("[Store Action] fetchQuesitosFromServer: API Erro!", err);
      set({ error: errorMessage, isLoading: false, currentFileBeingProcessed: null });
      console.log('[Store Action] fetchQuesitosFromServer: State atualizado com erro, isLoading false');
    }
  },

  uploadAndProcessSinglePdfForQuesitos: async (file: File, beneficio: string, profissao: string, modelo_nome: string) => {
    console.log('[Store Action] uploadAndProcessSinglePdfForQuesitos: Iniciando...');
    set({ isLoading: true, error: null, quesitosResult: null, processedDocumentInfo: null, currentFileBeingProcessed: file });
    console.log('[Store Action] uploadAndProcessSinglePdfForQuesitos: isLoading set to true, currentFile set');
    try {
      const processedDoc = await uploadAndProcessPdf(file); // Call new API function from api.ts
      console.log('[Store Action] uploadAndProcessSinglePdfForQuesitos: PDF processado!', processedDoc);
      set({ processedDocumentInfo: processedDoc });
      // Now call fetchQuesitosFromServer with the processedDoc.id
      await get().fetchQuesitosFromServer(processedDoc.id, beneficio, profissao, modelo_nome);
      // isLoading, error, quesitosResult will be set by fetchQuesitosFromServer
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Ocorreu um erro desconhecido durante o upload ou processamento do PDF.';
      console.error("[Store Action] uploadAndProcessSinglePdfForQuesitos: Erro no pipeline!", err);
      set({ error: errorMessage, isLoading: false, currentFileBeingProcessed: null });
      console.log('[Store Action] uploadAndProcessSinglePdfForQuesitos: State atualizado com erro, isLoading false');
    }
  },

  clearState: () => {
    console.log('[Store Action] clearState: Resetando estado.');
    set(initialState);
  },

}));