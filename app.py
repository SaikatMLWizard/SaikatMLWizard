import streamlit as st
import os
from assignment_rag import RAGDocumentAssistant # Or paste the class above here

# --- STREAMLIT USER INTERFACE CODE ---
st.set_page_config(page_title="Intelligent Omnichannel RAG", layout="wide")
st.title("📚 Intelligent Omnichannel Document Assistant")

st.sidebar.header("Data Sources")
data_folder = st.sidebar.text_input("Document Folder Path", value="./data")

# Multi-line input text area for entering web target links
web_links_input = st.sidebar.text_area(
    "Target Web URLs (One per line)", 
    value="https://en.wikipedia.org/wiki/Artificial_intelligence"
)
# Split the text string input into a structured python clean string list array
url_list = [url.strip() for url in web_links_input.split("\n") if url.strip()]

# OpenAI Authentication handling via Sidebar UI
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if api_key:
    os.environ["OPENAI_API_KEY"] = "sk-proj-eN47LV7bOZTh2hrkJZTniy8uOlURbA-z_bKkHeOllaqf2wsXcN1Ei32DlLXL23-AF1VM50nsnVT3BlbkFJasoyf1kmYhw-ZcaqzPqyVoHUp_4xcDw4L00278HBnmw-fd-Tlu8N1Yv3HZAnwFifITeC_XXXXX"

if "assistant" not in st.session_state:
    st.session_state.assistant = None

if st.sidebar.button("Build / Refresh Knowledge Engine"):
    if not os.environ.get("OPENAI_API_KEY"):
        st.sidebar.error("Missing OpenAI API Security Key Configuration!")
    else:
        with st.spinner("Processing local repository nodes & reading active web channels..."):
            try:
                assistant = RAGDocumentAssistant(data_dir=data_folder, web_urls=url_list)
                assistant.initialize_system()
                st.session_state.assistant = assistant
                st.sidebar.success("Unified Engine Active!")
            except Exception as e:
                st.sidebar.error(f"Initialization Fault: {str(e)}")

# Main Interface Application Window
user_query = st.text_input("Pose complex cross-document context or live URL data queries:")
if user_query:
    if st.session_state.assistant is None:
        st.warning("Please initialize the system from the sidebar configurations first.")
    else:
        with st.spinner("Executing hybrid retrieval search parameters..."):
            response = st.session_state.assistant.query(user_query)
            st.markdown("### 🤖 Response Layer Output:")
            st.write(response)