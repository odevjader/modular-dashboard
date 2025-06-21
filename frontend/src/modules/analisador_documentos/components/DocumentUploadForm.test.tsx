import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import DocumentUploadForm from './DocumentUploadForm';
import { useAnalisadorStore } from '../stores/analisadorStore';

// Mock the Zustand store
vi.mock('../stores/analisadorStore', () => ({
  useAnalisadorStore: vi.fn(),
}));

describe('DocumentUploadForm', () => {
  beforeEach(() => {
    // Reset mocks before each test
    vi.clearAllMocks();

    // Provide default mock implementation
    (useAnalisadorStore as any).mockReturnValue({
      setUploading: vi.fn(),
      setUploadSuccess: vi.fn(),
      resetState: vi.fn(),
      setUploadError: vi.fn(),
      status: 'idle', // Default status
      errorMessage: null,
      currentTaskId: null,
      pollingTimerId: null,
    });
  });

  it('renders the form with a file input and submit button', () => {
    render(<DocumentUploadForm />);

    // Check for the file input
    // The TextField component for file input doesn't directly support getByLabelText without a proper label.
    // We'll look for it by its role or a test ID if available.
    const fileInput = screen.getByTestId('file-input');
    expect(fileInput).toBeInTheDocument();


    // Check for the submit button
    const submitButton = screen.getByRole('button', { name: /enviar para análise/i });
    expect(submitButton).toBeInTheDocument();
  });
});
