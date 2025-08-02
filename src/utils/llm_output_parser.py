
# src/utils/llm_output_parser.py

import json
import re
from typing import Any, Optional
from .logger import get_logger

log = get_logger(__name__)

def extract_content_from_llm_output(output: Any) -> Optional[str]:
    """
    Robustly extracts the 'content' field from various LLM output formats.

    This function can handle:
    1. A Pydantic model object with a 'content' attribute.
    2. A dictionary with a 'content' key.
    3. A raw JSON string that needs to be cleaned and parsed.

    Args:
        output: The raw output from the LLM.

    Returns:
        The extracted content string, or None if it cannot be found.
    """
    # Case 1: Pydantic model or object with .content attribute
    if hasattr(output, 'content') and isinstance(output.content, str):
        return output.content

    # Case 2: Dictionary
    if isinstance(output, dict):
        return output.get("content")

    # Case 3: Raw string (potentially messy JSON)
    if isinstance(output, str):
        try:
            # Clean the string: find the first '{' and the last '}'
            match = re.search(r'\{.*\}', output, re.DOTALL)
            if match:
                clean_json_str = match.group(0)
                data = json.loads(clean_json_str)
                return data.get("content")
            else:
                log.warning(f"Could not find a JSON object in the LLM string output: {output}")
                return None
        except (json.JSONDecodeError, TypeError) as e:
            log.error(f"Failed to parse LLM string output as JSON: {e}. Output: '{output}'")
            return None
            
    log.warning(f"Unsupported output type for content extraction: {type(output)}")
    return None