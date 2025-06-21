import React, { useState, useCallback } from 'react';
import { Box, Button, TextField, Typography, CircularProgress } from '@mui/material';
import { uploadDocumentForAnalysis, DocumentUploadResponse } from '../../../services/api'; // Adjust path
import { useAnalisadorStore } from '../stores/analisadorStore'; // Import Zustand store

const DocumentUploadForm: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [localIsLoading, setLocalIsLoading] = useState<boolean>(false); // For the direct upload action
  const [localErrorMessage, setLocalErrorMessage] = useState<string|null>(null); // For file selection error

  const { setUploading, setUploadSuccess, resetState, setUploadError } = useAnalisadorStore(
    (state) => ({
      setUploading: state.setUploading,
      setUploadSuccess: state.setUploadSuccess,
      resetState: state.resetState,
      // Add a dedicated error action for upload failure for clarity
      setUploadError: (message: string) => state.status === 'uploading' && state.errorMessage === message ? undefined : useAnalisadorStore.setState({ status: 'error', errorMessage: message, currentTaskId: null, pollingTimerId: null }),
    })
  );

  // Get status to disable button if store is already processing something from another source (optional)
  const storeIsProcessing = useAnalisadorStore(state => state.status === 'uploading' || state.status === 'processing' || state.status === 'queued');


  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    resetState(); // Clear any previous state from the store
    setLocalErrorMessage(null);
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
    } else {
      setSelectedFile(null);
    }
  };

  const handleUpload = useCallback(async () => {
    if (!selectedFile) {
      setLocalErrorMessage('Por favor, selecione um arquivo PDF.');
      return;
    }
    setLocalErrorMessage(null);
    setLocalIsLoading(true);
    setUploading(); // Update store state to 'uploading'

    try {
      const response: DocumentUploadResponse = await uploadDocumentForAnalysis(selectedFile);
      // Pass message from gateway and task_id to the store
      setUploadSuccess(response.transcriber_data.task_id, `Upload de '${response.original_filename}' bem-sucedido. ${response.transcriber_data.message}`);
    } catch (error: any) {
      const apiErrorMessage = error.message || 'Falha no upload do arquivo.';
      setUploadError(apiErrorMessage); // Update store with error
      console.error('Upload error:', error);
    } finally {
      setLocalIsLoading(false);
    }
  }, [selectedFile, setUploading, setUploadSuccess, setUploadError, resetState]); // Added resetState to dependencies of handleFileChange indirectly via useEffect or direct call

  return (
    <Box component="div" sx={{ mt: 1 }}> {/* Changed from form as we handle submit via button click */}
      <Typography variant="subtitle1" gutterBottom>
        Selecione um arquivo PDF para análise:
      </Typography>
      <TextField
        type="file"
        onChange={handleFileChange}
        fullWidth
        variant="outlined"
        margin="normal"
        inputProps={{ accept: '.pdf', 'data-testid': 'file-input' }}
      />
      {selectedFile && (
        <Typography variant="body2" sx={{ mb: 2 }}>
          Arquivo selecionado: {selectedFile.name}
        </Typography>
      )}
       {localErrorMessage && <Typography color="error" sx={{ mb: 2 }}>{localErrorMessage}</Typography>}
      <Button
        variant="contained"
        color="primary"
        onClick={handleUpload}
        disabled={localIsLoading || !selectedFile || storeIsProcessing}
        sx={{ mt: 2, mb: 1 }}
      >
        {localIsLoading ? <CircularProgress size={24} /> : 'Enviar para Análise'}
      </Button>
      {/* Alert components for uploadMessage, errorMessage, taskId are removed
          as this feedback will be handled by ProcessingStatusIndicator via Zustand store. */}
    </Box>
  );
};

export default DocumentUploadForm;
