// frontend/src/modules/ai_test/AITestInterface.tsx
import React, { useState } from 'react';
import { postAITestPing, AITestInput, AITestResponse } from '../../services/api';
import {
    Box, TextField, Button, Typography, CircularProgress, Alert, Paper, Stack
} from '@mui/material';

// REMOVED: Reading model name from import.meta.env

const AITestInterface: React.FC = () => {
    const [prompt, setPrompt] = useState<string>('');
    const [aiResponse, setAiResponse] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const handlePromptChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setPrompt(event.target.value);
    };

    const handleSubmit = async () => {
        if (!prompt.trim()) {
            setError("Please enter a prompt.");
            return;
        }
        setLoading(true);
        setError(null);
        setAiResponse('');
        const payload: AITestInput = { text: prompt };

        try {
            const result: AITestResponse = await postAITestPing(payload);
            setAiResponse(result.response);
        } catch (err) {
            if (err instanceof Error) {
                setError(err.message);
            } else {
                setError('An unknown error occurred while communicating with the AI.');
            }
            console.error("Error in AI Test ping:", err);
        } finally {
            setLoading(false);
        }
    };

    // Construct the title with the hardcoded model name
    const title = `Módulo de teste IA (Langchain + gemini-2.0-flash-exp)`;

    return (
        <Stack spacing={3}>
            {/* Use the title with hardcoded model name */}
            <Typography variant="h6" component="h2">
                {title}
            </Typography>

            <TextField
                label="Enter your prompt/text here"
                multiline
                rows={4}
                value={prompt}
                onChange={handlePromptChange}
                variant="outlined"
                fullWidth
                disabled={loading}
            />

            <Box sx={{ textAlign: 'center' }}>
                <Button
                    variant="contained"
                    onClick={handleSubmit}
                    disabled={loading || !prompt.trim()}
                    sx={{ minWidth: '150px' }}
                >
                    {/* Keep updated Button Text */}
                    {loading ? <CircularProgress size={24} color="inherit" /> : 'manda bala'}
                </Button>
            </Box>

            {error && (
                <Alert severity="error" sx={{ mt: 2 }}>
                    {error}
                </Alert>
            )}

            {aiResponse && (
                <Paper elevation={2} sx={{ p: 2, mt: 2, whiteSpace: 'pre-wrap', bgcolor: 'grey.100' }}>
                    <Typography variant="subtitle1" gutterBottom>AI Response:</Typography>
                    <Typography variant="body1">{aiResponse}</Typography>
                </Paper>
            )}
        </Stack>
    );
};

export default AITestInterface;