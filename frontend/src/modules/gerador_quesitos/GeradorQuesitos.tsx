// frontend/src/modules/gerador_quesitos/GeradorQuesitos.tsx
import React, { useState, useRef, useCallback } from 'react';
import { postGerarQuesitos, RespostaQuesitos } from '../../services/api';
import {
    Box,
    Button,
    Typography,
    CircularProgress,
    Alert,
    Paper,
    Stack,
    Input, // Using Input for the hidden file input
    Link, // To show filename
} from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile'; // Icon for upload button

const GeradorQuesitos: React.FC = () => {
    // State for the selected file
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    // State for the AI's response
    const [respostaIA, setRespostaIA] = useState<string | null>(null);
    // State for loading indicator
    const [carregando, setCarregando] = useState<boolean>(false);
    // State for holding potential errors
    const [erro, setErro] = useState<string | null>(null);

    // Ref for the hidden file input element
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Handle file selection
    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file && file.type === 'application/pdf') {
            setSelectedFile(file);
            setErro(null); // Clear previous errors
            setRespostaIA(null); // Clear previous response
        } else {
            setSelectedFile(null);
            setErro('Por favor, selecione um arquivo PDF válido.');
            setRespostaIA(null);
        }
    };

    // Trigger hidden file input click
    const handleUploadClick = () => {
        fileInputRef.current?.click();
    };

    // Handle form submission (file upload and API call)
    const handleGerarQuesitos = useCallback(async () => {
        if (!selectedFile) {
            setErro("Nenhum arquivo PDF selecionado.");
            return;
        }

        setCarregando(true);
        setErro(null);
        setRespostaIA(null);

        const formData = new FormData();
        formData.append('file', selectedFile);
        // Append other Form data here if/when needed (e.g., profissao, grau)
        // formData.append('profissao', '...');

        try {
            const result: RespostaQuesitos = await postGerarQuesitos(formData);
            setRespostaIA(result.quesitos_texto);
        } catch (err) {
            if (err instanceof Error) {
                setErro(`Falha ao gerar quesitos: ${err.message}`);
            } else {
                setErro('Ocorreu um erro desconhecido ao gerar os quesitos.');
            }
            console.error("Erro ao gerar quesitos:", err);
        } finally {
            setCarregando(false);
        }
    }, [selectedFile]); // Dependency: re-create if selectedFile changes

    return (
        <Stack spacing={3}>
            <Typography variant="h6" component="h2">
                Gerador de Quesitos (Baseado em PDF)
            </Typography>

            {/* File Input Section */}
            <Box>
                <Button
                    variant="outlined"
                    onClick={handleUploadClick}
                    startIcon={<UploadFileIcon />}
                    disabled={carregando}
                >
                    Selecionar PDF
                </Button>
                {/* Hidden actual file input */}
                <Input
                    type="file"
                    inputRef={fileInputRef}
                    onChange={handleFileChange}
                    inputProps={{ accept: '.pdf' }} // Only accept PDF
                    sx={{ display: 'none' }} // Hide the default input
                />
                {/* Display selected filename */}
                {selectedFile && (
                    <Typography variant="body2" sx={{ ml: 2, display: 'inline' }}>
                        Arquivo: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)
                    </Typography>
                )}
            </Box>

            {/* Submit Button */}
            <Box sx={{ textAlign: 'center' }}>
                <Button
                    variant="contained"
                    onClick={handleGerarQuesitos}
                    disabled={carregando || !selectedFile}
                    sx={{ minWidth: '150px' }}
                >
                    {carregando ? <CircularProgress size={24} color="inherit" /> : 'Gerar Quesitos'}
                </Button>
            </Box>

            {/* Display Error if any */}
            {erro && (
                <Alert severity="error" sx={{ mt: 2 }}>
                    {erro}
                </Alert>
            )}

            {/* Display AI Response */}
            {respostaIA && (
                <Paper elevation={2} sx={{ p: 2, mt: 2, whiteSpace: 'pre-wrap', bgcolor: 'grey.100', maxHeight: '400px', overflowY: 'auto' }}>
                    <Typography variant="subtitle1" gutterBottom>Quesitos Gerados:</Typography>
                    <Typography variant="body2">{respostaIA}</Typography> {/* Use body2 for potentially long text */}
                </Paper>
            )}
        </Stack>
    );
};

export default GeradorQuesitos;