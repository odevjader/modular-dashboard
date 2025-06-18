import React, { useState } from 'react';
import { Box, Button, TextField, Typography, CircularProgress, Alert } from '@mui/material';
import { uploadDocumentForAnalysis, DocumentUploadResponse } from '../../../services/api'; // Adjust path if needed

const DocumentUploadForm: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);
  const [errorMesssage, setErrorMessage] = useState<string | null>(null);
  const [taskId, setTaskId] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
      setUploadMessage(null);
      setErrorMessage(null);
      setTaskId(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setErrorMessage('Por favor, selecione um arquivo PDF.');
      return;
    }

    setIsLoading(true);
    setUploadMessage(null);
    setErrorMessage(null);
    setTaskId(null);

    try {
      const response: DocumentUploadResponse = await uploadDocumentForAnalysis(selectedFile);
      setUploadMessage(`Arquivo '${response.original_filename}' enviado. ${response.transcriber_data.message}`);
      setTaskId(response.transcriber_data.task_id);
      // TODO: Store taskId in Zustand store for polling later
      console.log('Task ID for polling:', response.transcriber_data.task_id);
    } catch (error: any) {
      setErrorMessage(error.message || 'Falha no upload do arquivo.');
      console.error('Upload error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box component="form" noValidate autoComplete="off" sx={{ mt: 1 }}>
      <Typography variant="subtitle1" gutterBottom>
        Selecione um arquivo PDF para análise:
      </Typography>
      <TextField
        type="file"
        onChange={handleFileChange}
        fullWidth
        variant="outlined"
        margin="normal"
        inputProps={{ accept: '.pdf' }}
        // For better styling, consider using a styled Button that triggers a hidden input type="file"
      />
      {selectedFile && (
        <Typography variant="body2" sx={{ mb: 2 }}>
          Arquivo selecionado: {selectedFile.name}
        </Typography>
      )}
      <Button
        variant="contained"
        color="primary"
        onClick={handleUpload}
        disabled={isLoading || !selectedFile}
        sx={{ mt: 2, mb: 1 }}
      >
        {isLoading ? <CircularProgress size={24} /> : 'Enviar para Análise'}
      </Button>
      {uploadMessage && <Alert severity="success" sx={{ mt: 2 }}>{uploadMessage}</Alert>}
      {errorMesssage && <Alert severity="error" sx={{ mt: 2 }}>{errorMesssage}</Alert>}
      {taskId && <Alert severity="info" sx={{ mt: 2 }}>Task ID: {taskId} (para acompanhamento)</Alert>}
    </Box>
  );
};

export default DocumentUploadForm;
