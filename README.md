
# 📝 Blog Generation with LangGraph

## 🚀 Overview
This project is an agentic AI-powered blog generation system built with FastAPI, Streamlit, and LangGraph. It generates creative, SEO-friendly blog titles and detailed content based on a user-provided topic, with optional translation into Hindi or French. All generated blogs are automatically saved as Markdown files in a dedicated `blogs/` folder for easy access and management.

---

## ✨ Features
- Generate blog titles and content using advanced LLMs
- Translate blog content to Hindi and French (optional)
- Modular, graph-based workflow using LangGraph
- All generated blogs are saved as Markdown files in the `blogs/` directory
- User-friendly Streamlit web interface
- Robust logging and error handling
- Easily extendable for more languages and features

---

## 🗂️ Project Structure
```
app.py                # FastAPI backend (main entry point)
streamlit_app.py      # Streamlit web UI
src/
  llms/
    groqllm.py        # LLM integration
  graphs/
    graph_builder.py  # Graph construction logic
  nodes/
    blog_node.py      # Blog generation and translation nodes
  states/
    blogstate.py      # State management for blog generation
  utils/
    logger.py         # Logging utilities
    exception_handler.py # Custom exception handling
blogs/                # All generated blog Markdown files are saved here
requirements.txt      # Python dependencies
pyproject.toml        # Project metadata
README.md             # Project documentation
```

---

## ⚡ Getting Started
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

---

## 💡 Usage
1. Open the Streamlit link shown in your terminal (usually http://localhost:8501).
2. Enter a blog topic. (Language selection is optional; leave blank for default English.)
3. Click 'Generate Blog' to view the generated title and content.
4. Each generated blog is also saved as a Markdown file in the `blogs/` folder with a unique name.

---

## 🛠️ Extending & Customization
- Add new nodes in `src/nodes/` for additional features (e.g., more languages, summaries, etc.).
- Update `src/graphs/graph_builder.py` to modify or extend the workflow logic.
- Adjust logging or error handling in `src/utils/` as needed.

---

## 📁 Blog File Storage
- All generated blogs are saved in the `blogs/` directory as `.md` files.
- Filenames are based on the blog title and a timestamp for uniqueness.
- You can browse, edit, or use these Markdown files for publishing or further processing.

---

## 🤝 Contributing
Pull requests and suggestions are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

