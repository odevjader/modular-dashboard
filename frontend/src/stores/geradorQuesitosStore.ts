// frontend/src/stores/geradorQuesitosStore.ts
import { create } from 'zustand';
import { postGerarQuesitos, RespostaQuesitos } from '../services/api';

interface GeradorQuesitosState {
  isLoading: boolean;
  error: string | null;
  quesitosResult: string | null;
}

interface GeradorQuesitosActions {
  generateQuesitos: (formData: FormData) => Promise<void>;
  clearState: () => void;
}

const initialState: GeradorQuesitosState = {
  isLoading: false,
  error: null,
  quesitosResult: null,
};

export const useGeradorQuesitosStore = create<GeradorQuesitosState & GeradorQuesitosActions>((set) => ({
  ...initialState,

  generateQuesitos: async (formData: FormData) => {
    console.log('[Store Action] generateQuesitos: Iniciando...'); // Log Start
    set({ isLoading: true, error: null, quesitosResult: null });
    console.log('[Store Action] generateQuesitos: isLoading set to true'); // Log State Set

    try {
      console.log('[Store Action] generateQuesitos: Chamando postGerarQuesitos API...'); // Log API Call
      const result: RespostaQuesitos = await postGerarQuesitos(formData);
      console.log('[Store Action] generateQuesitos: API Sucesso!', result); // Log Success
      set({ quesitosResult: result.quesitos_texto, isLoading: false });
      console.log('[Store Action] generateQuesitos: State atualizado com sucesso, isLoading false'); // Log State Update Success
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Ocorreu um erro desconhecido.';
      console.error("[Store Action] generateQuesitos: API Erro!", err); // Log Error
      set({ error: errorMessage, isLoading: false });
       console.log('[Store Action] generateQuesitos: State atualizado com erro, isLoading false'); // Log State Update Error
    }
  },

  clearState: () => {
    console.log('[Store Action] clearState: Resetando estado.'); // Log Clear
    set(initialState);
  },

}));