import streamlit as st
import requests
import json
from src.utils.logger import get_logger

# --- Setup ---
log = get_logger(__name__)
st.set_page_config(page_title="Blog Generator", layout="centered")
st.title("AI Blog Generator ✨")
st.markdown("Generate creative, SEO-friendly blogs and translate them into Hindi or French!")

# --- User Input Form ---
with st.form("blog_form"):
    topic = st.text_input("Enter your blog topic:", placeholder="e.g., The Future of Renewable Energy")
    # Allow the user to select no language
    language_options = ["", "hindi", "french"]
    language = st.selectbox(
        "Select language (optional):", 
        language_options, 
        format_func=lambda x: "English (Default)" if x == "" else x.capitalize()
    )
    submitted = st.form_submit_button("Generate Blog")

# --- Backend Logic ---
if submitted:
    if not topic:
        st.warning("Please enter a blog topic to generate.")
    else:
        log.info(f"Form submitted with topic: '{topic}' and language: '{language}'")
        
        # Determine the display language for the spinner
        display_language = f' in {language.capitalize()}' if language else ''
        
        with st.spinner(f"Generating a blog about '{topic}'{display_language}... This may take a moment."):
            try:
                # Prepare the payload for the backend
                payload = {"topic": topic}
                if language:
                    payload["current_language"] = language
                
                # API Call with a generous timeout for the LLM
                response = requests.post(
                    "http://localhost:8000/blogs",
                    json=payload,
                    timeout=180  # Increased timeout to 3 minutes
                )
                response.raise_for_status()

                # --- Robust JSON Parsing ---
                response_json = response.json()
                log.info(f"Received JSON response from backend: {response_json}")

                # Safely navigate the JSON structure
                data = response_json.get("data", {})
                blog_data = data.get("blog", {})
                
                if not blog_data:
                    st.error("The backend returned a response, but it did not contain the expected blog data.")
                    log.error(f"Missing 'blog' key in response data: {data}")
                else:
                    title = blog_data.get("title", "No title generated.")
                    content = blog_data.get("content", "No content generated.")

                    st.subheader("📝 Generated Blog")
                    st.write(f"**Title:** {title}")
                    st.write(f"**Content:**")
                    st.markdown(content)

            except requests.exceptions.HTTPError as e:
                error_detail = "An unknown HTTP error occurred."
                try:
                    error_detail = e.response.json().get("detail", e.response.text)
                except json.JSONDecodeError:
                    error_detail = e.response.text
                st.error(f"Error from server: {error_detail}")
                log.error(f"HTTPError: {e.response.status_code} - {error_detail}")

            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend server. Please ensure it is running.")
                log.error("ConnectionError while trying to reach the backend.")
                
            except requests.exceptions.Timeout:
                st.error("The request timed out. The server might be busy or the topic is complex. Please try again.")
                log.error("Request to backend timed out.")

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                log.error(f"An unexpected error in Streamlit app: {e}", exc_info=True)
else:
    st.info("Enter a topic and click 'Generate Blog' to get started.")
