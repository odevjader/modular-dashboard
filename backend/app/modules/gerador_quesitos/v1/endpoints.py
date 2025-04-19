# backend/app/modules/gerador_quesitos/v1/endpoints.py
import os
import tempfile
from pathlib import Path
from fastapi import (
    APIRouter,
    HTTPException,
    status,
    File,
    UploadFile,
)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
# Use DoclingLoader for PDF processing
from langchain_docling import DoclingLoader # Corrected import if package name is langchain-docling

from core.config import settings, logger
from .esquemas import RespostaQuesitos

router = APIRouter()

# --- LLM Initialization ---
llm = None
if not settings.GOOGLE_API_KEY:
    logger.warning("GOOGLE_API_KEY not found. Gerador Quesitos module endpoints will not function.")
else:
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp", # Ensure this model supports the expected input/output
            google_api_key=settings.GOOGLE_API_KEY,
        )
        logger.info(f"ChatGoogleGenerativeAI initialized successfully for gerador_quesitos with model: {llm.model}")
    except Exception as e:
        logger.error(f"Failed to initialize ChatGoogleGenerativeAI for gerador_quesitos: {e}", exc_info=True)

# --- Load Prompt Template ---
prompt_template_string = ""
try:
    # Construct path relative to this file's location
    prompt_file_path = Path(__file__).parent / "prompts" / "gerar_quesitos_prompt.txt"
    if prompt_file_path.is_file():
        with open(prompt_file_path, "r", encoding="utf-8") as f:
            prompt_template_string = f.read()
        logger.info(f"Successfully loaded prompt template from {prompt_file_path}")
    else:
        logger.error(f"Prompt template file not found at {prompt_file_path}")
        # Decide how to handle missing prompt: raise error or use default? Raise for now.
        raise FileNotFoundError("Prompt template file missing.")
except Exception as e:
    logger.error(f"Failed to load prompt template: {e}", exc_info=True)
    # If prompt loading fails, the endpoint relying on it should probably not function
    # We could raise an error here or handle it within the endpoint. Let's handle in endpoint.


# --- API Endpoint ---
@router.post(
    "/gerar",
    response_model=RespostaQuesitos,
    summary="Gera quesitos periciais a partir de PDF.",
    tags=["Gerador Quesitos v1"],
)
async def gerar_quesitos(
    file: UploadFile = File(..., description="Documento PDF para análise.")
):
    """
    Recebe um PDF, extrai texto/OCR usando DoclingLoader,
    usa um prompt carregado de arquivo e exemplos para chamar Gemini via Langchain,
    e retorna os quesitos gerados.
    """
    if not llm:
        logger.error("LLM not initialized.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço de IA não configurado ou indisponível.",
        )

    if not prompt_template_string:
         logger.error("Prompt template not loaded.")
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno: Template de prompt não carregado.",
        )

    if file.content_type != "application/pdf":
        logger.warning(f"Invalid file type uploaded: {file.content_type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de arquivo inválido. Por favor, envie um PDF.",
        )

    # Use tempfile for secure temporary file handling
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            # Write uploaded file content to temp file
            content = await file.read()
            temp_pdf.write(content)
            temp_pdf_path = temp_pdf.name # Get the path
            logger.info(f"PDF saved temporarily to {temp_pdf_path}")

        # Use DoclingLoader on the temporary file path
        logger.info(f"Processing PDF with DoclingLoader: {temp_pdf_path}")
        # Check DoclingLoader options if needed (e.g., OCR settings)
        loader = DoclingLoader(file_path=temp_pdf_path) # Instantiate loader
        docs = await loader.aload() # Use async load if available, otherwise load()
        logger.info(f"DoclingLoader finished processing. Found {len(docs)} document sections.")

        # Combine extracted text (handle potential errors/empty docs)
        if not docs:
             logger.warning("DoclingLoader returned no document sections.")
             # Decide how to handle empty extraction: error or proceed with empty content?
             # Let's raise an error for now.
             raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Não foi possível extrair conteúdo do PDF fornecido.",
             )

        pdf_content_full = "\n\n".join([doc.page_content for doc in docs if doc.page_content])
        logger.info(f"Extracted text length: {len(pdf_content_full)}. Snippet: '{pdf_content_full[:100]}...'")

        if not pdf_content_full.strip():
             logger.warning("Extracted PDF content is empty or whitespace only.")
             raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="O conteúdo extraído do PDF está vazio.",
             )

        # Format the final prompt using the loaded template and extracted text
        # Note: Assumes template uses {pdf_content} placeholder.
        # Note: Few-shot examples are embedded in the template file itself per user request.
        final_prompt_text = prompt_template_string.format(pdf_content=pdf_content_full)

        # Create the message for Langchain
        # For Gemini models, especially multimodal, often just one HumanMessage is needed
        message = HumanMessage(content=final_prompt_text) # Sending combined text

        logger.info("Sending request to Gemini model via Langchain...")
        # Make the asynchronous call to the LLM
        ai_message = await llm.ainvoke([message]) # Pass message in a list
        texto_resposta = ai_message.content

        logger.info(f"Received AI response snippet: '{texto_resposta[:100]}...'")

        # Return the structured response
        return RespostaQuesitos(quesitos_texto=texto_resposta)

    except HTTPException:
         raise # Re-raise HTTP exceptions directly
    except Exception as e:
        logger.error(f"Error during quesitos generation: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar documento com o modelo de IA: {str(e)}",
        )
    finally:
        # Clean up the temporary file
        if 'temp_pdf_path' in locals() and os.path.exists(temp_pdf_path):
            try:
                os.remove(temp_pdf_path)
                logger.info(f"Deleted temporary file: {temp_pdf_path}")
            except Exception as e_del:
                logger.error(f"Error deleting temporary file {temp_pdf_path}: {e_del}")
        # Ensure uploaded file resource is closed if not already by context manager
        await file.close()