import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import DocumentUploadForm from '../../modules/analisador_documentos/components/DocumentUploadForm';
import ProcessingStatusIndicator from '../../modules/analisador_documentos/components/ProcessingStatusIndicator';

const AnalisadorDocumentosPage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Analisador de Documentos
      </Typography>
      <Box sx={{ mt: 2, p: 2, border: '1px dashed grey' }}>
        <Typography variant="h6" gutterBottom>Upload de Documento</Typography>
        <DocumentUploadForm />
      </Box>
      <Box sx={{ mt: 2, p: 2, border: '1px dashed grey' }}>
        {/* Typography for section title is in ProcessingStatusIndicator now, or can be added here if needed */}
        <ProcessingStatusIndicator />
      </Box>
      <Box sx={{ mt: 2, p: 2, border: '1px dashed grey' }}>
        <Typography variant="h6">Chat com Documento</Typography>
        <Typography variant="body2" color="text.secondary">
          (Placeholder para interface de chat)
        </Typography>
      </Box>
    </Container>
  );
};

export default AnalisadorDocumentosPage;
