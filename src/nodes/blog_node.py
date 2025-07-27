
from src.states.blogstate import BlogState
from src.states.blogstate import Blog
from src.utils.logger import get_logger

log = get_logger(__name__)

class BlogNode:
    """
    A class to represent he blog node
    """

    def __init__(self,llm):
        self.llm=llm

    
    def title_creation(self,state:BlogState):
        """
        create the title for the blog
        """

        if "topic" in state and state["topic"]:
            prompt="""
                   You are an expert blog content writer. Use Markdown formatting. Generate
                   a blog title for the {topic}. This title should be creative and SEO friendly

                   """
            
            system_message=prompt.format(topic=state["topic"])
            log.info(f"Generating title for topic: {state['topic']}")
            log.debug(f"System message for title creation: {system_message}")
            response = self.llm.invoke(system_message)
            log.info(f"Received response for title creation: {response.content}")
            return {"blog":{"title":response.content}}
        
    def content_generation(self,state:BlogState):
        if "topic" in state and state["topic"]:
            system_prompt = """You are expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic=state["topic"])
            log.info(f"Generating content for topic: {state['topic']}")
            response = self.llm.invoke(system_message)
            log.info("Received response for content generation:")
            return {"blog": {"title": state['blog']['title'], "content": response.content}}
    
    # Route to handle language translation
    def route(self,state:BlogState):
        log.info(f"Routing request for language: {state['current_language']}")
        return { "current_language": state["current_language"] }
    
    def route_decision(self, state: BlogState):
        """
        Decide the route based on the current language
        """
        log.info(f"Deciding route for language: {state['current_language']}")
        
        if state['current_language'] == 'hindi':
            return 'hindi'
        elif state['current_language'] == 'french':
            return 'french'
        else:
            return stat['current_language']
        

    
    def translation(self, state: BlogState):
        """
        Translate the content to the specified language.
        """
        translation_prompt = """
        Translate the following content into {current_language}.
        - Maintain the original tone, style, and formatting.
        - Adapt cultural references and idioms to be appropriate for {current_language}.
        - Return ONLY a valid JSON object with exactly two fields: 'title' and 'content'. Do not include any other fields or text.

        ORIGINAL CONTENT:
        {blog_content}
        """
        if not state.get('blog') or not state['blog'].get('content'):
            log.warning("No blog content available for translation.")
            
        blog_content = state['blog']['content']
        current_language = state['current_language']
        prompt = translation_prompt.format(current_language=current_language, blog_content=blog_content)
        result = self.llm.with_structured_output(Blog).invoke([prompt])
        log.info(f"Translation result: {result}")

        # Safety check for required fields
        if not hasattr(result, 'title') or not hasattr(result, 'content'):
            raise ValueError("LLM did not return both 'title' and 'content' fields. Got: {}".format(result))

        return {"blog": {"title": result.title, "content": result.content}}
        
        
        