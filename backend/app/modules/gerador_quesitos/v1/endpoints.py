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
)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.language_models.chat_models import BaseChatModel

# --- IMPORTS CORRIGIDOS ---
from app.core.config import settings, logger
from app.utils.pdf_processor import processar_pdfs_upload # Caminho absoluto
# --- FIM IMPORTS CORRIGIDOS ---
from .esquemas import RespostaQuesitos # Relativo ok

router = APIRouter()

# --- Default LLM Initialization (from settings) ---
default_llm: Optional[BaseChatModel] = None
default_model_name = settings.GEMINI_MODEL_NAME
if not settings.GOOGLE_API_KEY:
    logger.warning("GOOGLE_API_KEY not found. Default LLM for Gerador Quesitos will not function.")
else:
    try:
        default_llm = ChatGoogleGenerativeAI(
            model=default_model_name,
            google_api_key=settings.GOOGLE_API_KEY,
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
        try:
            llm_to_use = ChatGoogleGenerativeAI(
                model=modelo_nome,
                google_api_key=settings.GOOGLE_API_KEY,
            )
            selected_model_display_name = modelo_nome
            logger.info(f"Dynamically initialized LLM with model: {modelo_nome}")
        except Exception as e:
            logger.error(f"Failed to initialize requested LLM model '{modelo_nome}': {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Não foi possível inicializar o modelo de IA solicitado: '{modelo_nome}'. Verifique se o nome está correto e disponível."
            )

    if not llm_to_use:
        logger.error("LLM instance is unavailable (Default failed and no specific model requested/initialized).")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Serviço de IA indisponível.")

    # --- Process Files ---
    try:
        logger.info(f"Calling shared PDF processor for {len(files)} file(s)...")
        texto_extraido_combinado = await processar_pdfs_upload(files)

        if not texto_extraido_combinado:
             logger.warning("PDF processing utility returned no text.")
             raise HTTPException(
                 status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                 detail="Não foi possível extrair conteúdo válido dos PDFs fornecidos.",
             )
        logger.info(f"PDF processing complete. Total text length: {len(texto_extraido_combinado)}")

        # --- Format Prompt ---
        final_prompt_text = prompt_template_string.format(
            pdf_content=texto_extraido_combinado,
            beneficio=beneficio,
            profissao=profissao
        )

        # --- Call LLM ---
        message = HumanMessage(content=final_prompt_text)
        logger.info(f"Sending request to Gemini model '{selected_model_display_name}' via Langchain...")
        ai_message = await llm_to_use.ainvoke([message])
        texto_resposta = ai_message.content
        logger.info(f"Received AI response snippet: '{texto_resposta[:100]}...'")

        # --- Return Response ---
        return RespostaQuesitos(quesitos_texto=texto_resposta)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unhandled error during quesitos generation: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado ao gerar quesitos: {str(e)}",
        )