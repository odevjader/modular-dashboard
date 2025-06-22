// frontend/src/modules/gerador_quesitos/GeradorQuesitos.tsx
import React, { useState, useRef, ChangeEvent, useEffect } from 'react';
import {
    Box, Button, Typography, CircularProgress, Alert, Paper, Stack,
    Input, List, ListItem, ListItemText, IconButton, Select, MenuItem,
    FormControl, InputLabel, SelectChangeEvent, Fade
} from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import DeleteIcon from '@mui/icons-material/Delete';
import { OPCOES_BENEFICIO, OPCOES_PROFISSAO, OPCOES_MODELO_IA, FRASES_DIVERTIDAS } from '../../config/opcoesFormulario';
import { useGeradorQuesitosStore } from '../../stores/geradorQuesitosStore';
// ProcessedDocumentInfo might be useful here for display, but not directly used in actions
// import { ProcessedDocumentInfo } from '../../services/api';

const GeradorQuesitos: React.FC = () => {
    // Local state
    const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
    const [beneficio, setBeneficio] = useState<string>('');
    const [profissao, setProfissao] = useState<string>('');
    const [modeloIASelecionado, setModeloIASelecionado] = useState<string>(OPCOES_MODELO_IA[0]);
    const [uiMessage, setUiMessage] = useState<string | null>(null);
    const [fraseDivertida, setFraseDivertida] = useState<string>('');
    const fileInputRef = useRef<HTMLInputElement>(null);
    const intervalRef = useRef<NodeJS.Timeout | null>(null);

    // Global state
    const {
        isLoading, error, quesitosResult,
        uploadAndProcessSinglePdfForQuesitos, // New action
        currentFileBeingProcessed, // New state
        processedDocumentInfo // New state
    } = useGeradorQuesitosStore();

    // Effect for funny phrases
    useEffect(() => {
        if (isLoading) {
            setFraseDivertida(FRASES_DIVERTIDAS[Math.floor(Math.random() * FRASES_DIVERTIDAS.length)]);
            intervalRef.current = setInterval(() => {
                setFraseDivertida(currentPhrase => {
                    let newPhrase;
                    do {
                        newPhrase = FRASES_DIVERTIDAS[Math.floor(Math.random() * FRASES_DIVERTIDAS.length)];
                    } while (newPhrase === currentPhrase && FRASES_DIVERTIDAS.length > 1);
                    return newPhrase;
                });
            }, 4000);
        } else {
            if (intervalRef.current) { clearInterval(intervalRef.current); intervalRef.current = null; }
            setFraseDivertida('');
        }
        return () => { if (intervalRef.current) { clearInterval(intervalRef.current); } };
    }, [isLoading]);

    // Handlers
    const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
        const files = event.target.files;
        let newFilesToAdd: File[] = [];
        let skippedCount = 0;
        let nonPdfCount = 0;
        setUiMessage(null);
        if (files) {
            const potentialFiles = Array.from(files);
            potentialFiles.forEach(file => {
                if (file.type !== 'application/pdf') { nonPdfCount++; return; }
                const isDuplicate = selectedFiles.some(
                    existingFile => existingFile.name === file.name && existingFile.size === file.size
                );
                if (isDuplicate) { skippedCount++; } else { newFilesToAdd.push(file); }
            });
            if (newFilesToAdd.length > 0) { setSelectedFiles(prevFiles => [...prevFiles, ...newFilesToAdd]); }
            let message = '';
            if (nonPdfCount > 0) { message += `${nonPdfCount} arquivo(s) ignorado(s) por não ser(em) PDF. `; }
            if (skippedCount > 0) { message += `${skippedCount} arquivo(s) duplicado(s) ignorado(s).`; }
            setUiMessage(message.trim() || null);
        }
        if (fileInputRef.current) { fileInputRef.current.value = ''; }
    };
    const handleUploadClick = () => { fileInputRef.current?.click(); };
    const handleRemoveFile = (indexToRemove: number) => { setSelectedFiles(prevFiles => prevFiles.filter((_, index) => index !== indexToRemove)); };
    const handleBeneficioChange = (event: SelectChangeEvent<string>) => { setBeneficio(event.target.value as string); };
    const handleProfissaoChange = (event: SelectChangeEvent<string>) => { setProfissao(event.target.value as string); };
    const handleModeloIAChange = (event: SelectChangeEvent<string>) => { setModeloIASelecionado(event.target.value as string); };

    const handleGerarQuesitos = () => {
        setUiMessage(null);
        if (selectedFiles.length === 0) {
            setUiMessage("Nenhum arquivo PDF selecionado.");
            return;
        }
        if (selectedFiles.length > 1) {
            setUiMessage("Apenas o primeiro arquivo PDF selecionado será processado para esta funcionalidade.");
            // Continue with the first file
        }
        if (!beneficio) { setUiMessage("Por favor, selecione o benefício."); return; }
        if (!profissao) { setUiMessage("Por favor, selecione a profissão."); return; }

        const fileToProcess = selectedFiles[0];

        uploadAndProcessSinglePdfForQuesitos(fileToProcess, beneficio, profissao, modeloIASelecionado);
    };

    return (
        <Stack spacing={3}>
            <Typography variant="h6" component="h2"> Gerador de quesitos </Typography>
            {!isLoading ? ( /* Inputs */ <>
                <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
                   <FormControl fullWidth required error={!!uiMessage && !beneficio}>
                       <InputLabel id="beneficio-select-label">Benefício Pretendido</InputLabel>
                       <Select labelId="beneficio-select-label" value={beneficio} label="Benefício Pretendido" onChange={handleBeneficioChange} disabled={isLoading}>
                           {OPCOES_BENEFICIO.map((option) => (<MenuItem key={option} value={option}>{option}</MenuItem>))}
                       </Select>
                   </FormControl>
                    <FormControl fullWidth required error={!!uiMessage && !profissao}>
                       <InputLabel id="profissao-select-label">Profissão</InputLabel>
                       <Select labelId="profissao-select-label" value={profissao} label="Profissão" onChange={handleProfissaoChange} disabled={isLoading}>
                           {OPCOES_PROFISSAO.map((option) => (<MenuItem key={option} value={option}>{option}</MenuItem>))}
                       </Select>
                   </FormControl>
                </Stack>
                <FormControl fullWidth>
                   <InputLabel id="modelo-ia-select-label">Modelo IA (Opcional)</InputLabel>
                   <Select labelId="modelo-ia-select-label" value={modeloIASelecionado} label="Modelo IA (Opcional)" onChange={handleModeloIAChange} disabled={isLoading}>
                       {OPCOES_MODELO_IA.map((option) => ( <MenuItem key={option} value={option}> {option === "<Modelo Padrão>" ? <em>{option}</em> : option} </MenuItem> ))}
                   </Select>
                </FormControl>
               <Box>
                   <Button variant="outlined" onClick={handleUploadClick} startIcon={<UploadFileIcon />} disabled={isLoading}> Adicionar PDF(s) </Button>
                   <Input type="file" inputRef={fileInputRef} onChange={handleFileChange} inputProps={{ accept: '.pdf', multiple: true }} sx={{ display: 'none' }} />
               </Box>
            </> ) : ( /* Loading State Display */
                <Paper elevation={0} sx={{ p: 2, textAlign: 'center', bgcolor: 'action.hover' }}>
                    <Typography variant="h5" component="p" gutterBottom>
                        { currentFileBeingProcessed ? `Processando: ${currentFileBeingProcessed.name}` : "Gerando Quesitos..."}
                    </Typography>
                    { currentFileBeingProcessed && processedDocumentInfo && (
                        <Typography variant="caption" display="block" color="text.secondary" sx={{mb:1}}>
                           Arquivo processado: ID {processedDocumentInfo.id}, Hash: ...{processedDocumentInfo.file_hash.slice(-8)}
                        </Typography>
                    )}
                    <Typography variant="body1" color="text.secondary"> Benefício: {beneficio} </Typography>
                    <Typography variant="body1" color="text.secondary"> Profissão: {profissao} </Typography>
                    <Typography variant="body1" color="text.secondary"> Modelo: {modeloIASelecionado} </Typography>
                </Paper>
            )}
            {selectedFiles.length > 0 && ( /* File List */ <Paper variant="outlined" sx={{ p: 1, mt: 1, maxHeight: '200px', overflowY: 'auto' }}>
                 <Typography variant="subtitle2" gutterBottom sx={{ pl: 1 }}>
                     {selectedFiles.length > 1 ? `Arquivo para processar: ${selectedFiles[0].name} (de ${selectedFiles.length} selecionados)` : `Arquivo Selecionado: ${selectedFiles[0].name}`}
                 </Typography>
                <List dense>
                    {selectedFiles.map((file, index) => (
                        <ListItem key={`${file.name}-${index}-${file.lastModified}`} secondaryAction={ <IconButton edge="end" aria-label="delete" onClick={() => handleRemoveFile(index)} disabled={isLoading}> <DeleteIcon fontSize="small"/> </IconButton> } sx={{py: 0}}>
                            <ListItemText primary={file.name} secondary={`${(file.size / 1024).toFixed(1)} KB`} primaryTypographyProps={{ sx: { overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' } }} />
                        </ListItem>
                    ))}
                </List>
            </Paper> )}
             {uiMessage && !isLoading && ( <Alert severity={uiMessage.includes('duplicado') || uiMessage.includes('ignorados') ? 'info' : 'warning'} sx={{ mt: 1 }}> {uiMessage} </Alert> )}
            <Box sx={{ textAlign: 'center', mt: 2 }}> {/* Submit Button */}
                <Button variant="contained" color="primary" onClick={handleGerarQuesitos} disabled={isLoading || selectedFiles.length === 0 || !beneficio || !profissao} sx={{ minWidth: '180px', px: 3, py: 1.5, fontSize: '1rem' }}>
                    {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Gerar Quesitos'}
                </Button>
            </Box>
            {/* Display Funny Phrase during loading - CHANGED variant to body1 */}
            {isLoading && (
                 <Fade in={!!fraseDivertida} timeout={300}>
                     <Box>
                         <Typography variant="body1" /* Changed from caption */ align="center" sx={{ mt: 1, fontStyle: 'italic', display: 'block', minHeight: '1.5em' /* Adjusted minHeight */ }}>
                             {fraseDivertida || '\u00A0'}
                         </Typography>
                     </Box>
                </Fade>
            )}
            {error && ( /* API Error */ <Alert severity="error" sx={{ mt: 2 }}> {error} </Alert> )}
            {quesitosResult && !isLoading && ( /* Result */ <Paper elevation={2} sx={{ p: 2, mt: 2, whiteSpace: 'pre-wrap', bgcolor: 'grey.100', maxHeight: '500px', overflowY: 'auto' }}> <Typography variant="subtitle1" gutterBottom>Quesitos Gerados:</Typography> <Typography variant="body2">{quesitosResult}</Typography> </Paper> )}
        </Stack>
    );
};

export default GeradorQuesitos;