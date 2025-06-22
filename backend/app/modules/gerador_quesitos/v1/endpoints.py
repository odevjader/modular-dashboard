# backend/app/modules/gerador_quesitos/v1/endpoints.py
from pathlib import Path
from typing import List, Optional
from fastapi import (
    APIRouter,
    HTTPException,
    status,
    File,
    UploadFile,
    Form,
    Depends, # Added Depends
)
from langchain_google_genai import ChatGoogleGenerativeAI # Uncommented/Added
from langchain_core.messages import HumanMessage # Uncommented/Added
from langchain_core.language_models.chat_models import BaseChatModel # Uncommented/Added
from sqlalchemy.orm import Session # Added for DB session
from app.core.database import get_db # Added for DB dependency
from app.models.document import Document, DocumentChunk # Added for DB query

# --- IMPORTS CORRIGIDOS ---
from app.core.config import settings, logger
# TODO: Funcionalidade desativada temporariamente (Fase 1 Roadmap - Refatoração Core).
# Dependências removidas do container API (Docling/Tesseract). Será reimplementado via serviço dedicado na Fase 2.
# Código original comentando abaixo:
# from app.utils.pdf_processor import processar_pdfs_upload # Caminho absoluto
# --- FIM IMPORTS CORRIGIDOS ---
from . import esquemas # Updated to import the whole module
from .esquemas import RespostaQuesitos # Relativo ok

router = APIRouter()

# --- Default LLM Initialization (from settings) ---
# This will be used if specific model is not requested or if "<Modelo Padrão>" is chosen.
default_llm: Optional[BaseChatModel] = None
default_model_name = settings.GEMINI_MODEL_NAME
if not settings.GOOGLE_API_KEY:
    logger.warning("GOOGLE_API_KEY not found. Default LLM for Gerador Quesitos will not function.")
else:
    try:
        default_llm = ChatGoogleGenerativeAI(
            model=default_model_name,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.7, # Example: Adjust temperature if needed
            # top_p=0.9, # Example: Adjust top_p if needed
            # top_k=40   # Example: Adjust top_k if needed
        )
        logger.info(f"Default LLM initialized successfully for gerador_quesitos with model: {default_model_name}")
    except Exception as e:
        logger.error(f"Failed to initialize default LLM for gerador_quesitos with model {default_model_name}: {e}", exc_info=True)
        # default_llm remains None

# --- Load Prompt Template ---
prompt_template_string = ""
prompt_file_path = Path(__file__).parent / "prompts" / "gerar_quesitos_prompt.txt"
try:
    if not prompt_file_path.is_file():
        raise FileNotFoundError(f"Prompt template file missing at {prompt_file_path}")
    with open(prompt_file_path, "r", encoding="utf-8") as f:
        prompt_template_string = f.read()
    logger.info(f"Successfully loaded prompt template from {prompt_file_path}")
except Exception as e:
    logger.error(f"CRITICAL: Failed to load prompt template on startup: {e}", exc_info=True)
    prompt_template_string = ""


# --- API Endpoint ---
@router.post(
    "/gerar",
    response_model=RespostaQuesitos,
    summary="Gera quesitos periciais a partir de múltiplos PDFs e informações do caso, com seleção de modelo.",
    tags=["Gerador Quesitos"], # Tag simplificada
)
async def gerar_quesitos(
    files: List[UploadFile] = File(..., description="Um ou mais documentos PDF para análise."),
    beneficio: str = Form(..., description="Benefício previdenciário pretendido."),
    profissao: str = Form(..., description="Profissão do requerente."),
    modelo_nome: str = Form(..., description="Nome do modelo de IA a ser usado ou '<Modelo Padrão>."),
):
    """
    Recebe PDFs e info, chama utilitário para extrair texto, formata prompt,
    chama o modelo Gemini selecionado (ou padrão) via Langchain, e retorna os quesitos gerados.
    """
    if not prompt_template_string:
          logger.error("Prompt template not loaded during startup.")
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno: Template de prompt não disponível.")
    if not files:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum arquivo PDF enviado.")

    logger.info(f"Received request. Beneficio: {beneficio}, Profissao: {profissao}, Model: {modelo_nome}, Files: {[f.filename for f in files]}")

    # --- Select or Initialize LLM ---
    llm_to_use: Optional[BaseChatModel] = None
    selected_model_display_name = ""

    if modelo_nome == "<Modelo Padrão>" or not modelo_nome:
        logger.info(f"Using default LLM model: {default_model_name}")
        llm_to_use = default_llm
        selected_model_display_name = default_model_name
    else:
        logger.info(f"Attempting to use specifically requested LLM model: {modelo_nome}")
        if not settings.GOOGLE_API_KEY:
             logger.error("Cannot initialize specific model: GOOGLE_API_KEY not found.")
             raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Serviço de IA não configurado (chave API ausente).")
        # TODO: Funcionalidade desativada temporariamente (Fase 1 Roadmap - Refatoração Core).
        # Dependências removidas do container API. Será movida para um serviço dedicado na Fase 2.
        # Código original comentando abaixo:
        # try:
        #     # TODO: Funcionalidade desativada temporariamente (Fase 1 Roadmap - Refatoração Core).
        #     # Dependências removidas do container API. Será movida para um serviço dedicado na Fase 2.
        #     # Código original comentando abaixo:
        #     # llm_to_use = ChatGoogleGenerativeAI(
        #     #     model=modelo_nome,
        #     #     google_api_key=settings.GOOGLE_API_KEY,
        #     # )
        #     # selected_model_display_name = modelo_nome
        #     # logger.info(f"Dynamically initialized LLM with model: {modelo_nome}")
        # # TODO: Funcionalidade desativada temporariamente (Fase 1 Roadmap - Refatoração Core).
        # # Dependências removidas do container API. Será movida para um serviço dedicado na Fase 2.
        # # Código original comentando abaixo:
        # # except Exception as e:
        # #     logger.error(f"Failed to initialize requested LLM model '{modelo_nome}': {e}", exc_info=True)
        # #     raise HTTPException(
        # #         status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        # #         detail=f"Não foi possível inicializar o modelo de IA solicitado: '{modelo_nome}'. Verifique se o nome está correto e disponível."
        # #     )

    # TODO: Funcionalidade desativada temporariamente (Fase 1 Roadmap - Refatoração Core).
    # Dependências removidas do container API. Será movida para um serviço dedicado na Fase 2.
    # Código original comentando abaixo:
    # if not llm_to_use:
    #     logger.error("LLM instance is unavailable (Default failed and no specific model requested/initialized).")
    #     raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Serviço de IA indisponível.")

    # --- Process Files ---
    # TODO: Funcionalidade desativada temporariamente (Fase 1 Roadmap - Refatoração Core).
    # Dependências removidas do container API (Docling/Tesseract). Será reimplementado via serviço dedicado na Fase 2.
    # Código original comentando abaixo:
    # try:
    #     logger.info(f"Calling shared PDF processor for {len(files)} file(s)...")
    #     texto_extraido_combinado = await processar_pdfs_upload(files)
    #
    #     if not texto_extraido_combinado:
    #          logger.warning("PDF processing utility returned no text.")
    #          raise HTTPException(
    #              status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #              detail="Não foi possível extrair conteúdo válido dos PDFs fornecidos.",
    #          )
    #     logger.info(f"PDF processing complete. Total text length: {len(texto_extraido_combinado)}")
    #
    #     # --- Format Prompt ---
    #     final_prompt_text = prompt_template_string.format(
    #         pdf_content=texto_extraido_combinado,
    #         beneficio=beneficio,
    #         profissao=profissao
    #     )
    #
    #     # --- Call LLM ---
    #     message = HumanMessage(content=final_prompt_text)
    #     logger.info(f"Sending request to Gemini model '{selected_model_display_name}' via Langchain...")
    #     # TODO: Funcionalidade desativada temporariamente (Fase 1 Roadmap - Refatoração Core).
    #     # Dependências removidas do container API. Será movida para um serviço dedicado na Fase 2.
    #     # Código original comentando abaixo:
    #     # ai_message = await llm_to_use.ainvoke([message])
    #     # texto_resposta = ai_message.content
    #     # logger.info(f"Received AI response snippet: '{texto_resposta[:100]}...'")
    #     texto_resposta = "Funcionalidade de geração de quesitos via IA desativada temporariamente." # Placeholder response
    #
    #     # --- Return Response ---
    #     return RespostaQuesitos(quesitos_texto=texto_resposta)
    #
    # except HTTPException:
    #     raise
    # except Exception as e:
    #     logger.error(f"Unhandled error during quesitos generation: {e}", exc_info=True)
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f"Erro inesperado ao gerar quesitos: {str(e)}",
    #     )
    texto_resposta = "Funcionalidade de geração de quesitos via IA desativada temporariamente." # Placeholder response
    return RespostaQuesitos(quesitos_texto=texto_resposta)


@router.post(
    "/gerar_com_referencia_documento",
    response_model=RespostaQuesitos,
    summary="Gera quesitos a partir de um ID de documento pré-processado.",
    tags=["Gerador Quesitos"],
)
async def gerar_quesitos_com_referencia(
    payload: esquemas.GerarQuesitosComDocIdPayload,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_active_user) # Add if auth is needed here
):
    if not prompt_template_string:
        logger.error("Prompt template not loaded during startup.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno: Template de prompt não disponível.")

    logger.info(f"Received request for doc_id: {payload.document_id}, Beneficio: {payload.beneficio}, Profissao: {payload.profissao}, Model: {payload.modelo_nome}")

    # 1. Fetch document chunks from DB
    # Assuming Document and DocumentChunk are imported from app.models.document
    # MODIFIED: Query directly the 'documents' table used by transcritor_pdf_service
    # This table stores chunks directly, with 'filename' and 'text_content'.
    # We'll order by page number and then by an assumed original chunk index if available in metadata.
    from sqlalchemy import text

    # The 'documents' table from transcritor_pdf has:
    # chunk_id TEXT PK, filename TEXT, page_number INTEGER (in metadata),
    # text_content TEXT, metadata JSONB (containing page_number, original_chunk_index_on_page)
    # embedding VECTOR, created_at TIMESTAMP

    # Ensure the table name and column names are correct as per transcritor_pdf's main.py setup.
    # The startup event in transcritor_pdf/src/main.py creates 'documents' table.
    # Metadata stores filename and page_number. Let's assume 'original_chunk_index_on_page' is also there.

    query_str = """
        SELECT text_content
        FROM documents
        WHERE filename = :doc_filename
        ORDER BY (metadata->>'page_number')::INT, (metadata->>'original_chunk_index_on_page')::INT NULLS LAST;
    """
    # NULLS LAST in case original_chunk_index_on_page is not always present

    stmt = text(query_str).bindparams(doc_filename=payload.document_filename)

    try:
        result = await db.execute(stmt)
        # result will be a CursorResult, iterate over it to get rows
        # Each row will be a RowProxy-like object where text_content is the first element
        chunk_texts = [row[0] for row in result.fetchall()] # Assuming text_content is the first column selected
    except Exception as e:
        logger.error(f"Database error when fetching chunks for filename {payload.document_filename}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao buscar conteúdo do documento no banco de dados.")


    if not chunk_texts:
        logger.warning(f"Nenhum chunk encontrado para document_filename: {payload.document_filename}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Documento com nome '{payload.document_filename}' não encontrado ou não possui conteúdo processado.")

    texto_extraido_combinado = "\n\n".join(chunk_texts)
    logger.info(f"Retrieved and combined {len(chunk_texts)} chunks for doc_filename {payload.document_filename}. Total text length: {len(texto_extraido_combinado)}")

    # 2. Select LLM
    llm_to_use: Optional[BaseChatModel] = None
    selected_model_display_name = ""
    # default_model_name is already defined globally

    if payload.modelo_nome == "<Modelo Padrão>" or not payload.modelo_nome:
        logger.info(f"Using default LLM model: {default_model_name}")
        llm_to_use = default_llm # Use the globally initialized default_llm
        selected_model_display_name = default_model_name
        if not llm_to_use: # Check if default_llm failed to initialize
             logger.warning("Default LLM was not available. Attempting to re-initialize for this request.")
             if settings.GOOGLE_API_KEY:
                 try:
                     llm_to_use = ChatGoogleGenerativeAI(model=default_model_name, google_api_key=settings.GOOGLE_API_KEY)
                     selected_model_display_name = default_model_name
                 except Exception as e:
                     logger.error(f"Failed to re-initialize default LLM {default_model_name}: {e}")
             else:
                 logger.warning("GOOGLE_API_KEY not found for default LLM in gerar_quesitos_com_referencia")

    else:
        logger.info(f"Attempting to use specifically requested LLM model: {payload.modelo_nome}")
        if not settings.GOOGLE_API_KEY:
            logger.error("Cannot initialize specific model: GOOGLE_API_KEY not found.")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Serviço de IA não configurado (chave API ausente).")
        try:
            llm_to_use = ChatGoogleGenerativeAI(model=payload.modelo_nome, google_api_key=settings.GOOGLE_API_KEY)
            selected_model_display_name = payload.modelo_nome
            logger.info(f"Dynamically initialized LLM with model: {payload.modelo_nome}")
        except Exception as e:
            logger.error(f"Failed to initialize requested LLM model '{payload.modelo_nome}': {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Não foi possível inicializar o modelo de IA solicitado: '{payload.modelo_nome}'."
            )

    if not llm_to_use:
        logger.error("LLM instance is unavailable.")
        logger.warning("LLM is unavailable. Returning placeholder response for quesitos.")
        return RespostaQuesitos(quesitos_texto="Placeholder: LLM indisponível, quesitos não gerados.")

    # 3. Format Prompt
    final_prompt_text = prompt_template_string.format(
        pdf_content=texto_extraido_combinado,
        beneficio=payload.beneficio,
        profissao=payload.profissao
    )

    # 4. Call LLM
    message = HumanMessage(content=final_prompt_text)
    logger.info(f"Sending request to Gemini model '{selected_model_display_name}' via Langchain...")
    try:
        ai_message = await llm_to_use.ainvoke([message])
        texto_resposta = ai_message.content
        logger.info(f"Received AI response snippet: '{texto_resposta[:100]}...'" )
    except Exception as e:
        logger.error(f"Error during LLM call: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao contatar o serviço de IA: {str(e)}")

    return RespostaQuesitos(quesitos_texto=texto_resposta)