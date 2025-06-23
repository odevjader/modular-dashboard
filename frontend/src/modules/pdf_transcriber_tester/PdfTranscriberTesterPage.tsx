import React, { useState, useEffect, useCallback } from 'react';
import {
  Container,
  Typography,
  Button,
  Paper,
  Box,
  CircularProgress,
  Alert,
  TextField,
  Grid,
} from '@mui/material';
import { useSnackbar } from 'notistack';
import { uploadDocumentForAnalysis, getTaskStatus, DocumentUploadResponse, TaskStatusResponse } from '../../services/api'; // Adjust path as needed

const PdfTranscriberTesterPage: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [transcriptionStatus, setTranscriptionStatus] = useState<string | null>(null);
  const [transcriptionResult, setTranscriptionResult] = useState<string | null>(null);
  const [pollingError, setPollingError] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [isPolling, setIsPolling] = useState<boolean>(false);

  const { enqueueSnackbar } = useSnackbar();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
      setUploadStatus('idle');
      setUploadError(null);
      setTaskId(null);
      setTranscriptionStatus(null);
      setTranscriptionResult(null);
      setPollingError(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      enqueueSnackbar('Please select a PDF file first.', { variant: 'warning' });
      return;
    }

    setIsUploading(true);
    setUploadStatus('uploading');
    setUploadError(null);
    setTaskId(null); // Reset previous task ID

    try {
      const response: DocumentUploadResponse = await uploadDocumentForAnalysis(selectedFile);
      setUploadStatus('success');
      enqueueSnackbar(response.message || 'File uploaded successfully! Transcription started.', { variant: 'success' });
      if (response.transcriber_data && response.transcriber_data.task_id) {
        setTaskId(response.transcriber_data.task_id);
      } else {
        setUploadStatus('error');
        setUploadError('Task ID not found in upload response.');
        enqueueSnackbar('Task ID not found in upload response.', { variant: 'error' });
      }
    } catch (error: any) {
      setUploadStatus('error');
      const errorMessage = error.message || 'File upload failed.';
      setUploadError(errorMessage);
      enqueueSnackbar(errorMessage, { variant: 'error' });
    } finally {
      setIsUploading(false);
    }
  };

  // useCallback to memoize poll function
  const pollStatus = useCallback(async (currentTaskId: string) => {
    try {
      const statusResponse: TaskStatusResponse = await getTaskStatus(currentTaskId);
      setTranscriptionStatus(statusResponse.status);

      if (statusResponse.status === 'SUCCESS') {
        setTranscriptionResult(JSON.stringify(statusResponse.result, null, 2) || 'Transcription successful, but no result content.');
        enqueueSnackbar('Transcription completed successfully!', { variant: 'success' });
        return true; // Stop polling
      } else if (statusResponse.status === 'FAILURE') {
        setPollingError(statusResponse.error_info?.error || 'Transcription failed for an unknown reason.');
        setTranscriptionResult(JSON.stringify(statusResponse.error_info, null, 2) || 'Failure details unavailable.');
        enqueueSnackbar('Transcription failed.', { variant: 'error' });
        return true; // Stop polling
      }
      return false; // Continue polling
    } catch (error: any) {
      const errorMessage = error.message || 'Failed to fetch transcription status.';
      setPollingError(errorMessage);
      enqueueSnackbar(errorMessage, { variant: 'error' });
      return true; // Stop polling on error
    }
  }, [enqueueSnackbar]);


  useEffect(() => {
    let intervalId: NodeJS.Timeout | undefined = undefined;

    if (taskId && (transcriptionStatus !== 'SUCCESS' && transcriptionStatus !== 'FAILURE')) {
      setIsPolling(true);
      // Initial poll
      pollStatus(taskId).then(stop => {
        if (stop) setIsPolling(false);
      });

      intervalId = setInterval(async () => {
        const stopPolling = await pollStatus(taskId);
        if (stopPolling) {
          clearInterval(intervalId);
          setIsPolling(false);
        }
      }, 5000); // Poll every 5 seconds
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
      setIsPolling(false); // Ensure polling stops on cleanup
    };
  }, [taskId, pollStatus, transcriptionStatus]);


  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          PDF Transcriber Tester
        </Typography>

        <Grid container spacing={2} alignItems="center" sx={{ mb: 2 }}>
          <Grid item xs={12} sm={8}>
            <TextField
              type="file"
              onChange={handleFileChange}
              fullWidth
              variant="outlined"
              size="small"
              InputLabelProps={{ shrink: true }}
              inputProps={{ accept: '.pdf' }}
              label={selectedFile ? selectedFile.name : "Select PDF File"}
            />
          </Grid>
          <Grid item xs={12} sm={4}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleUpload}
              disabled={!selectedFile || isUploading || isPolling}
              fullWidth
              startIcon={isUploading ? <CircularProgress size={20} color="inherit" /> : null}
            >
              {isUploading ? 'Uploading...' : 'Upload & Transcribe'}
            </Button>
          </Grid>
        </Grid>

        {uploadStatus === 'error' && uploadError && (
          <Alert severity="error" sx={{ mb: 2 }}>{uploadError}</Alert>
        )}

        {taskId && (
          <Box sx={{ mt: 2, p: 2, border: '1px dashed grey', borderRadius: 1 }}>
            <Typography variant="h6">Transcription Progress</Typography>
            <Typography variant="body2">Task ID: {taskId}</Typography>
            <Typography variant="body2">
              Status: {transcriptionStatus || 'Fetching status...'}
              {isPolling && <CircularProgress size={16} sx={{ ml: 1 }} />}
            </Typography>
            {pollingError && (
              <Alert severity="error" sx={{ mt: 1 }}>Polling Error: {pollingError}</Alert>
            )}
          </Box>
        )}

        {transcriptionResult && (
          <Box sx={{ mt: 2, p: 2, border: '1px solid green', borderRadius: 1 }}>
            <Typography variant="h6">Transcription Result</Typography>
            <TextField
              value={transcriptionResult}
              multiline
              fullWidth
              rows={10}
              variant="outlined"
              InputProps={{ readOnly: true }}
              sx={{ mt: 1, fontFamily: 'monospace' }}
            />
          </Box>
        )}
      </Paper>
    </Container>
  );
};

export default PdfTranscriberTesterPage;
