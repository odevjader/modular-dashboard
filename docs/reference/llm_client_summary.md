# LLM Client (`llm_client.py`) Summary

This document provides a summary of the `transcritor-pdf/src/extractor/llm_client.py` module, which is responsible for configuring and providing a Large Language Model (LLM) client.

## Main Purpose

The primary purpose of `llm_client.py` is to:
- Securely load LLM API credentials (API key, base URL, model name) from environment variables, typically defined in a `.env` file.
- Initialize a Langchain chat model client, specifically `langchain_openai.ChatOpenAI`. This client is compatible with OpenAI's API standards, making it suitable for use with various LLM providers like OpenRouter.ai.
- Provide a singleton instance of the initialized client through the `get_llm_client()` function. This ensures that the configuration is loaded and the client is initialized only once during the application's lifecycle.

## Configuration

The module is configured primarily through environment variables, which can be conveniently managed using a `.env` file in the project root or an accessible parent directory.

Key environment variables include:

-   **`OPENAI_API_KEY` (Mandatory)**: Your API key for the LLM provider. The script will raise a `ValueError` if this is not found.
-   **`OPENAI_BASE_URL` (Optional)**: The base URL for the LLM provider's API.
    *   Defaults to: `https://openrouter.ai/api/v1` (a common OpenRouter URL).
-   **`OPENAI_MODEL_NAME` (Optional)**: The primary environment variable for specifying the model name.
-   **`OPENROUTER_MODEL_NAME` (Optional)**: An alternative environment variable for specifying the model name.
    *   If neither `OPENAI_MODEL_NAME` nor `OPENROUTER_MODEL_NAME` is set, it defaults to: `google/gemini-flash`.

The module uses `python-dotenv` to load variables from a `.env` file. It searches for this file up the directory tree from the script's location.

## Main Function: `get_llm_client()`

The core function for obtaining an LLM client instance is `get_llm_client()`.

-   **Singleton Behavior**: This function implements a singleton pattern. The `ChatOpenAI` client is initialized only upon the first call. Subsequent calls return the same cached instance, preventing redundant initializations and configuration loading.
-   **Return Value**: It returns an initialized instance of `langchain_openai.ChatOpenAI`, configured with the API key, base URL, and model name retrieved from the environment variables.

## Key Dependencies

The module relies on the following key Python libraries:

-   **`python-dotenv`**: For loading environment variables from a `.env` file.
-   **`langchain-openai`**: For providing the `ChatOpenAI` client, which is used to interact with LLM providers that adhere to the OpenAI API specification. (The script will exit if this library is not found).

## Basic Error Handling

The module includes basic error handling:

-   **Missing API Key**: If the `OPENAI_API_KEY` environment variable is not set, `load_api_config()` (called by `get_llm_client()`) will log a critical error and raise a `ValueError`.
-   **Initialization Failures**: `get_llm_client()` catches general exceptions during client initialization, logs them, and re-raises them as a `RuntimeError`.
-   **Missing `langchain-openai`**: If the `langchain-openai` library is not installed, a critical error is logged, and the script exits.

## Usage Example

Here's a conceptual Python code example demonstrating how to import and use `get_llm_client()` to obtain an LLM client and make a simple call:

```python
import logging
# Adjust the import path based on your project structure and how llm_client.py is accessible.
# For example, if 'transcritor-pdf/src' is in your PYTHONPATH:
# from extractor.llm_client import get_llm_client
# Or, if llm_client.py is part of an installable package 'my_package':
# from my_package.extractor.llm_client import get_llm_client

# For this example, let's assume direct relative import if this script is placed appropriately,
# or that the module is discoverable via PYTHONPATH.
# The original script uses: from transcritor_pdf.src.extractor.llm_client import get_llm_client
# We will use a placeholder import for this conceptual example.
# Ensure you adapt this to your specific project setup.

# Placeholder for the actual import - replace with your project's structure
# from your_project_module.llm_client import get_llm_client
# For testing this snippet independently, you might need to add the parent directory to sys.path
# import sys
# sys.path.append('../path/to/transcritor-pdf/src') # Adjust as needed
from extractor.llm_client import get_llm_client


# It's good practice to configure logging to see outputs from the client module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Example of how to get and use the LLM client.
    Make sure your .env file is set up with OPENAI_API_KEY.
    """
    try:
        logger.info("Attempting to retrieve the LLM client...")
        # This is where you would call the actual get_llm_client function
        # For the purpose of this example, we'll assume it's imported correctly.
        llm = get_llm_client()
        logger.info("LLM client retrieved successfully.")

        # Example of making a simple call (requires langchain-core for ChatPromptTemplate)
        # This part is conceptual and depends on having langchain-core components.
        try:
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_core.messages import SystemMessage, HumanMessage

            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content="You are a helpful assistant that provides concise answers."),
                HumanMessage(content="What is the capital of France?")
            ])

            # Create a simple chain
            chain = prompt | llm

            logger.info("Making a call to the LLM...")
            # For prompts without input variables, use an empty dict.
            # If your prompt template was e.g. ("user", "{user_question}"),
            # you would use: chain.invoke({"user_question": "What is the capital of France?"})
            response = chain.invoke({})

            if hasattr(response, 'content'):
                logger.info(f"LLM Response: {response.content}")
            else:
                logger.info(f"LLM Response (raw): {response}")

        except ImportError:
            logger.warning("Skipping LLM call example: langchain-core components not found.")
        except Exception as e:
            logger.error(f"Error during LLM call: {e}", exc_info=True)

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
    except RuntimeError as e:
        logger.error(f"Runtime error during client initialization: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    # Note: To run this example, you'd need to:
    # 1. Have a .env file with at least OPENAI_API_KEY.
    # 2. Have langchain-openai and langchain-core installed.
    # 3. Adjust the import path for get_llm_client based on your project structure.
    #    The placeholder `from extractor.llm_client import get_llm_client` assumes
    #    that the 'transcritor-pdf/src' directory is in the Python path.
    main()
```

This summary should help users understand and utilize the `llm_client.py` module effectively.
