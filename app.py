import uvicorn
from fastapi import FastAPI, Request
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM
from src.utils.logger import get_logger
from src.utils.exception_handler import api_exception_handler, generic_exception_handler
from src.utils.exceptions import APIException, InvalidRequestError


import os
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
log = get_logger(__name__)
app = FastAPI()

# Register exception handlers
app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

print(os.getenv("LANGCHAIN_API_KEY"))
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

@app.post("/blogs")
async def create_blogs(request: Request):
    """
    Endpoint to generate a blog post based on a topic.
    """
    try:
        data = await request.json()
        topic = data.get("topic", "")
        current_language = data.get("current_language", "").lower()

        if not topic:
            raise InvalidRequestError("Topic is required to generate a blog.")
        
        log.info(f"Received request to generate blog for topic: {topic} and language: {current_language}")

        groqllm = GroqLLM()
        llm = groqllm.get_llm()
        graph_builder = GraphBuilder(llm)


        if topic and current_language:
            graph = graph_builder.setup_graph(usecase="language")
            state = graph.invoke({"topic": topic, "current_language": current_language})
        elif topic:
            graph = graph_builder.setup_graph(usecase="topic")
            state = graph.invoke({"topic": topic, "current_language": current_language.lower()})
            log.info(f"Successfully generated blog for topic: {topic}")

        # Save blog to file if generated
        blog = state.get("blog", {})
        title = blog.get("title", "untitled-blog")
        content = blog.get("content", "")
        # Sanitize title for filename
        safe_title = re.sub(r'[^a-zA-Z0-9_-]', '_', title)[:50]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"blogs/{safe_title}_{timestamp}.md"
        os.makedirs("blogs", exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n{content}")
        log.info(f"Blog saved to {filename}")

        return {"data": state}

    except APIException as e:
        # This will be handled by your custom handler, but you can log here if you want
        log.error(f"APIException: {e.detail}")
        raise
    except Exception as e:
        log.error(f"Unhandled Exception: {e}")
        raise

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)