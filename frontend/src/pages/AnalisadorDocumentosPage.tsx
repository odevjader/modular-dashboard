import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, TextField, Button, List, ListItem, Paper, Tooltip } from '@mui/material';
import DocumentUploadForm from '../../modules/analisador_documentos/components/DocumentUploadForm';
import ProcessingStatusIndicator from '../../modules/analisador_documentos/components/ProcessingStatusIndicator';
import { useAnalisadorStore } from '../../modules/analisador_documentos/stores/analisadorStore';
import { postDocumentQuery, DocumentQueryPayload, DocumentQueryResponse } from '../../services/api';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
}

const AnalisadorDocumentosPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [userInput, setUserInput] = useState('');
  const [isSending, setIsSending] = useState(false);
  const { processedDocumentId, status: docStatus } = useAnalisadorStore();

  const chatDisabled = docStatus !== 'success' || !processedDocumentId;
  let placeholderText = "Digite sua mensagem...";
  if (docStatus === 'pending' || docStatus === 'processing') {
    placeholderText = "Aguarde o processamento do documento para interagir.";
  } else if (docStatus === 'failed') {
    placeholderText = "Falha no processamento do documento. Não é possível interagir.";
  } else if (!processedDocumentId && docStatus === 'success') {
    // This case might indicate an issue or that no document was ever processed.
    placeholderText = "Documento processado, mas ID não encontrado. Não é possível interagir.";
  } else if (!processedDocumentId) {
    placeholderText = "Nenhum documento processado. Faça upload de um documento para interagir.";
  }


  const handleSendMessage = async () => {
    if (userInput.trim() === '' || isSending || chatDisabled) {
      return;
    }

    setIsSending(true);
    const userMessageText = userInput;
    const newMessage: Message = { id: Date.now().toString(), text: userMessageText, sender: 'user' };
    setMessages(prevMessages => [...prevMessages, newMessage]);
    setUserInput('');

    try {
      if (!processedDocumentId) { // Should be caught by chatDisabled, but as a safeguard
        throw new Error("processedDocumentId is not available.");
      }
      const payload: DocumentQueryPayload = { query_text: userMessageText };
      const response = await postDocumentQuery(processedDocumentId, payload);
      const aiResponse: Message = { id: response.query_id || Date.now().toString(), text: response.answer, sender: 'ai' };
      setMessages(prevMessages => [...prevMessages, aiResponse]);
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        text: "Desculpe, não consegui processar sua pergunta. Tente novamente mais tarde.",
        sender: 'ai'
      };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsSending(false);
    }
  };

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
        <ProcessingStatusIndicator />
      </Box>
      <Box sx={{ mt: 2, p: 2, border: '1px dashed grey' }}>
        <Typography variant="h6" gutterBottom>Chat com Documento</Typography>
        <Paper sx={{ height: '400px', overflowY: 'auto', p: 2, mb: 2 }}>
          <List>
            {messages.map((msg) => (
              <ListItem key={msg.id} sx={{
                justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                mb: 1,
              }}>
                <Paper
                  elevation={3}
                  sx={{
                    p: 1.5,
                    bgcolor: msg.sender === 'user' ? 'primary.light' : 'secondary.light',
                    color: msg.sender === 'user' ? 'primary.contrastText' : 'secondary.contrastText',
                    maxWidth: '70%',
                    wordBreak: 'break-word',
                  }}
                >
                  <Typography variant="body1">{msg.text}</Typography>
                </Paper>
              </ListItem>
            ))}
          </List>
        </Paper>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder={placeholderText}
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            disabled={isSending || chatDisabled}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !isSending && userInput.trim() !== '' && !chatDisabled) {
                handleSendMessage();
              }
            }}
            sx={{ mr: 1 }}
          />
          <Tooltip title={chatDisabled ? placeholderText : "Enviar mensagem"}>
            <span> {/* Span needed for Tooltip when button is disabled */}
              <Button
                variant="contained"
                color="primary"
                onClick={handleSendMessage}
                disabled={isSending || userInput.trim() === '' || chatDisabled}
              >
                Enviar
              </Button>
            </span>
          </Tooltip>
        </Box>
      </Box>
    </Container>
  );
};

export default AnalisadorDocumentosPage;
