# backend/app/modules/ai_test/v1/endpoints.py
from fastapi import APIRouter, HTTPException, status
from langchain_google_genai import ChatGoogleGenerativeAI

# --- IMPORT CORRIGIDO ---
from app.core.config import settings, logger # Import settings using absolute path
# --- FIM IMPORT CORRIGIDO ---
from .schemas import TextInput, AIResponse # Import the schemas (relative is OK)

# Define the router for this module
router = APIRouter()

# Initialize the LLM
llm = None
llm_error = None # Store potential initialization error

if settings.GOOGLE_API_KEY:
    try:
        llm = ChatGoogleGenerativeAI(
            # Using model specified in settings or fallback
            model=settings.GEMINI_MODEL_NAME or "gemini-2.0-flash-exp", # Use setting
            google_api_key=settings.GOOGLE_API_KEY,
            # convert_system_message_to_human=True # Example optional arg
        )
        logger.info(f"ChatGoogleGenerativeAI initialized successfully for ai_test with model: {settings.GEMINI_MODEL_NAME or 'gemini-2.0-flash-exp'}")
    except Exception as e:
        logger.error(f"Failed to initialize ChatGoogleGenerativeAI for ai_test: {e}", exc_info=True)
        llm_error = str(e)
else:
    logger.warning("GOOGLE_API_KEY not found. AI Test module endpoints will not function.")
    llm_error = "GOOGLE_API_KEY not configured."


@router.post("/ping",
             response_model=AIResponse,
             summary="Send a 'ping' text to the AI model",
             tags=["AI Test"]) # Simplified Tag
async def ping_ai_model(input_data: TextInput):
    """
    Receives text input, sends it to the configured Google Gemini model
    via Langchain, and returns the response.
    """
    if not llm:
        logger.error(f"Attempted to use /ping endpoint but LLM is not initialized. Error: {llm_error}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI model is not configured or available. Check API key. Error: {llm_error}"
        )

    logger.info(f"Received AI ping request with text: '{input_data.text[:50]}...'")

    try:
        # Use Langchain's async invoke method
        ai_message = await llm.ainvoke(input_data.text)
        response_text = ai_message.content
        logger.info(f"Received AI response: '{response_text[:50]}...'")
        return AIResponse(response=response_text)

    except Exception as e:
        logger.error(f"Error during AI model invocation: {e}", exc_info=True)
        error_detail = f"An error occurred while processing with the AI model: {str(e)}"
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail
        )