import React from 'react';
import { Box, Typography, LinearProgress, Alert } from '@mui/material';
import { useAnalisadorStore } from '../stores/analisadorStore'; // Adjust path

const ProcessingStatusIndicator: React.FC = () => {
  const { status, progress, statusMessage, errorMessage, currentTaskId } = useAnalisadorStore(
    (state) => ({
      status: state.status,
      progress: state.progress,
      statusMessage: state.statusMessage,
      errorMessage: state.errorMessage,
      currentTaskId: state.currentTaskId,
    })
  );

  if (status === 'idle' && !currentTaskId) { // Only hide if truly idle and no task ever started
    return null;
  }

  return (
    <Box sx={{ width: '100%', mt: 2 }}> {/* Removed border for cleaner look, page has it */}
      <Typography variant="h6" gutterBottom>Status do Processamento</Typography>

      {statusMessage && <Typography variant="body1" gutterBottom>{statusMessage}</Typography>}

      {(status === 'uploading' || status === 'processing' || status === 'queued') && (
        <Box sx={{ display: 'flex', alignItems: 'center', mt: 1, mb: 1 }}>
          <Box sx={{ width: '100%', mr: 1 }}>
            <LinearProgress
              variant={progress >= 0 && progress <= 100 ? "determinate" : "indeterminate"}
              value={(progress >= 0 && progress <= 100) ? progress : undefined}
            />
          </Box>
          {(progress >= 0 && progress <=100) && (status === 'processing' || status === 'queued' || status === 'uploading') && (
            <Box sx={{ minWidth: 35 }}>
              <Typography variant="body2" color="text.secondary">{`${Math.round(progress)}%`}</Typography>
            </Box>
          )}
        </Box>
      )}

      {errorMessage && <Alert severity="error" sx={{ mt: 1 }}>{errorMessage}</Alert>}

      {status === 'success' && !errorMessage && (
        <Alert severity="success" sx={{ mt: 1 }}>
          {statusMessage || 'Documento processado com sucesso!'}
        </Alert>
      )}
    </Box>
  );
};

export default ProcessingStatusIndicator;
