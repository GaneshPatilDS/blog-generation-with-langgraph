# Blog Generation with LangGraph

## Overview
This project is an agentic AI-powered blog generation system using LangGraph. It generates creative, SEO-friendly blog titles and detailed content based on a given topic, with support for translation into multiple languages (Hindi, French, etc.).

## Features
- Generate blog titles and content using LLMs
- Translate blog content to Hindi and French
- Modular graph-based workflow using LangGraph
- Easily extendable for more languages and features

## Project Structure
```
app.py                # Main entry point
src/
  llms/
    groqllm.py        # LLM integration
  graphs/
    graph_builder.py  # Graph construction logic
  nodes/
    blog_node.py      # Blog generation and translation nodes
  states/
    blogstate.py      # State management for blog generation
requirements.txt      # Python dependencies
pyproject.toml        # Project metadata
README.md             # Project documentation
```


## Getting Started
1. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   pip install streamlit
   ```
2. **Start the FastAPI backend**:
   ```powershell
   python app.py
   ```
3. **Run the Streamlit UI**:
   ```powershell
   streamlit run streamlit_app.py
   ```

## Usage
- Open the Streamlit link shown in your terminal (usually http://localhost:8501).
- Enter a topic and select a language (English, Hindi, French).
- Click 'Generate Blog' to view the generated title and content.

## Extending
- Add new nodes in `src/nodes/` for additional features.
- Update `src/graphs/graph_builder.py` to modify graph logic.


