# src/nodes/blog_node.py

# Import the robust LLM output parser utility
from src.utils.llm_output_parser import extract_content_from_llm_output

from src.states.blogstate import BlogState
from src.utils.logger import get_logger
from pydantic import BaseModel, Field

log = get_logger(__name__)

class BlogNode:
    """A class to represent the blog generation and translation nodes."""

    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state: BlogState):
        """Creates the title for the blog."""
        if "topic" not in state or not state["topic"]:
            log.warning("No topic found in state for title creation.")
            return {}

        prompt = f"""
        You are an expert blog title writer.
        Generate a single, creative, and SEO-friendly blog title for the topic: '{state["topic"]}'.
        Return only the title text, with no extra formatting or quotation marks.
        """
        log.info(f"Generating title for topic: {state['topic']}")
        response = self.llm.invoke(prompt)
        # Clean up the response to remove potential extra quotes
        cleaned_title = response.content.strip().replace('"', '')
        log.info(f"Generated title: {cleaned_title}")
        return {"blog": {"title": cleaned_title}}

    def content_generation(self, state: BlogState):
        """Generates the main content for the blog."""
        if "topic" not in state or not state["topic"]:
            log.warning("No topic found in state for content generation.")
            return {}

        system_prompt = f"""
        You are an expert blog writer. Use Markdown formatting.
        Generate a detailed blog post of around 500 words with a clear breakdown for the topic: '{state["topic"]}'.
        """
        log.info(f"Generating content for topic: {state['topic']}")
        response = self.llm.invoke(system_prompt)
        log.info("Successfully generated blog content.")
        return {"blog": {"title": state['blog']['title'], "content": response.content}}

    def route(self, state: BlogState):
        """A passthrough node to log the routing request before decision."""
        log.info(f"Routing request for language: {state['current_language']}")
        # This node simply passes the state along. The decision is next.
        return {}

    def route_decision(self, state: BlogState):
        """Decides the route based on the current language."""
        language = state.get('current_language', 'english').lower()
        log.info(f"Routing decision for language: {language}")
        if language in ['hindi', 'french']:
            return language
        return 'end'  # End the process if no translation is needed

    def translation(self, state: BlogState):
        """Translates the content to the specified language, paragraph by paragraph."""

        # --- Define Pydantic models INSIDE the function scope for reliability ---
        class ParagraphTranslation(BaseModel):
            """A model to hold translated paragraph content."""
            content: str = Field(description="The translated paragraph text.")

        class TitleTranslation(BaseModel):
            """A model to hold the translated title."""
            title: str = Field(description="The translated blog title.")
        # ---------------------------------------------------------------------

        if not state.get('blog') or not state['blog'].get('content'):
            log.warning("No blog content available for translation.")
            return {}

        blog_content = state['blog']['content']
        current_language = state['current_language']
        log.info(f"Starting translation to {current_language}.")

        # --- Translate Title ---
        try:
            title_prompt = f"""
            Translate the following blog title to {current_language}.
            You MUST use the 'TitleTranslation' tool to format your response.
            Title: {state['blog']['title']}
            """
            llm_with_title_parser = self.llm.with_structured_output(TitleTranslation)
            title_result = llm_with_title_parser.invoke(title_prompt)
            translated_title = title_result.title
            log.info(f"Successfully translated title: {translated_title}")
        except Exception as e:
            log.error(f"Title translation failed, using original. Error: {e}")
            translated_title = state['blog']['title'] # Fallback to original title

        # --- Translate Content ---
        paragraphs = [p.strip() for p in blog_content.split('\n\n') if p.strip()]
        translated_paragraphs = []
        
        llm_with_paragraph_parser = self.llm.with_structured_output(ParagraphTranslation)

        for i, para in enumerate(paragraphs):
            try:
                paragraph_prompt = f"""
                Translate the following paragraph to {current_language}.
                Maintain the original tone and Markdown formatting.
                You MUST use the 'ParagraphTranslation' tool to format your response.
                Paragraph:
                ---
                {para}
                ---
                """
                result = llm_with_paragraph_parser.invoke(paragraph_prompt)
                translated_paragraphs.append(result.content)
            except Exception as e:
                log.error(f"Translation failed at paragraph {i}, using original. Error: {e}")
                translated_paragraphs.append(para) # Fallback to original paragraph

        translated_content = "\n\n".join(translated_paragraphs)
        log.info(f"Finished translation to {current_language}.")

        return {"blog": {"title": translated_title, "content": translated_content}}
