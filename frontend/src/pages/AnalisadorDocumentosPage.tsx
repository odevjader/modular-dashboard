import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import DocumentUploadForm from '../../modules/analisador_documentos/components/DocumentUploadForm';

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
        <Typography variant="h6">Status do Processamento</Typography>
        <Typography variant="body2" color="text.secondary">
          (Placeholder para indicador de status)
        </Typography>
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
