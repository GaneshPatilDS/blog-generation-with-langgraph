
# import necessary libraries
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from src.utils.logger import log # Assuming 'log' is your configured logger
from src.utils.exceptions import LLMConnectionError

# Best practice to load environment variables once at the start
load_dotenv()

class GroqLLM:
    """A wrapper for the ChatGroq LLM to ensure robust initialization."""
    
    def __init__(self, model_name: str = "llama-3.1-8b-instant"):
        self.model_name = model_name
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        """
        Private method to get the API key and initialize the LLM.
        This isolates the initialization logic.
        """
        try:
            
            # 1. Get the API key cleanly
            api_key = os.getenv("GROQ_API_KEY")
            log.info("getting api key")
            
            # 2. Validate the API key
            if not api_key:
                log.error("GROQ_API_KEY environment variable is not set.")
                # Raise the exception directly. No need to catch it here.
                raise LLMConnectionError("GROQ_API_KEY is not set.")
            log.info("API key retrieved successfully.")

            # 3. Initialize the LLM
            log.info(f"Initializing ChatGroq model: {self.model_name}")
            llm = ChatGroq(api_key=api_key, model=self.model_name)
            log.info("ChatGroq model initialized successfully.")
            return llm

        # 4. Catch any other unexpected errors during initialization
        except Exception as e:
            log.error(f"An unexpected error occurred while setting up the LLM: {e}", exc_info=True)
            # Wrap the original exception for better error context
            raise LLMConnectionError(detail=f"Failed to initialize LLM. Original error: {e}")

    def get_llm(self):
        """Public method to return the initialized LLM instance."""
        log.info("Returning the initialized LLM instance.")
        return self.llm
        
    
    