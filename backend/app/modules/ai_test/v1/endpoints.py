# backend/app/modules/ai_test/v1/endpoints.py
from fastapi import APIRouter, HTTPException, status
from langchain_google_genai import ChatGoogleGenerativeAI

from core.config import settings, logger # Import settings and logger
from .schemas import TextInput, AIResponse # Import the schemas

# Define the router for this module
router = APIRouter()

# Initialize the LLM
llm = None
if settings.GOOGLE_API_KEY:
    try:
        # Initialize using the user-specified model name
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp", # UPDATED to specific experimental model
            google_api_key=settings.GOOGLE_API_KEY
        )
        logger.info(f"ChatGoogleGenerativeAI initialized successfully with model: {llm.model}")
    except Exception as e:
        logger.error(f"Failed to initialize ChatGoogleGenerativeAI: {e}")
else:
    logger.warning("GOOGLE_API_KEY not found. AI Test module endpoints will not function.")


@router.post("/ping",
             response_model=AIResponse,
             summary="Send a 'ping' text to the AI model",
             tags=["AI Test v1"])
async def ping_ai_model(input_data: TextInput):
    """
    Receives text input ('ping' or other test prompt), sends it to the
    configured Google Gemini model via Langchain, and returns the response.
    """
    if not llm:
        logger.error("Attempted to use /ping endpoint but LLM is not initialized.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI model is not configured or available. Check API key."
        )

    logger.info(f"Received AI ping request with text: '{input_data.text[:50]}...'")

    try:
        # Use Langchain's invoke method
        ai_message = await llm.ainvoke(input_data.text) # Use async invoke
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