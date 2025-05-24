import streamlit as st
from PyPDF2 import PdfReader 
from langchain.text_splitter import CharacterTextSplitter 
from langchain.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
import os
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv() 
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 

def main():
    print("hello word")
    st.set_page_config(
        page_title="ASK PDF",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }
    
    /* Dynamic background that works in both light and dark mode */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    [data-theme="light"] .stApp {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
    }
    
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    [data-theme="light"] .main-header {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient 3s ease infinite;
        margin-bottom: 0.3rem;
    }
    
    .subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 400;
    }
    
    [data-theme="light"] .subtitle {
        color: rgba(0, 0, 0, 0.7);
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .upload-section {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin: 1rem 0;
        text-align: center;
    }
    
    [data-theme="light"] .upload-section {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    /* Enhanced Upload Card */
    .upload-card-wrapper {
        margin: 1rem 0 0.5rem 0;
    }
    
    .upload-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        border: 2px dashed rgba(255, 255, 255, 0.4);
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    [data-theme="light"] .upload-card {
        background: rgba(255, 255, 255, 0.9);
        border: 2px dashed rgba(0, 0, 0, 0.3);
    }
    
    .upload-card:hover {
        border-color: #4ecdc4;
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    [data-theme="light"] .upload-card:hover {
        background: rgba(255, 255, 255, 0.95);
        border-color: #2196f3;
    }
    
    .upload-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .upload-card:hover::before {
        left: 100%;
    }
    
    .upload-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        opacity: 0.8;
    }
    
    .stats-container {
        display: flex;
        justify-content: center;
        margin: 1rem 0;
        gap: 0.8rem;
        max-width: 300px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 0.8rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.3);
        flex: 1;
        min-width: 70px;
    }
    
    [data-theme="light"] .stat-card {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    .stat-value {
        font-size: 1.3rem;
        font-weight: bold;
        color: #4ecdc4;
        margin-bottom: 0.2rem;
    }
    
    [data-theme="light"] .stat-value {
        color: #2196f3;
    }
    
    .stat-label {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.75rem;
    }
    
    [data-theme="light"] .stat-label {
        color: rgba(0, 0, 0, 0.7);
    }
    
    /* Prominent Chat Section */
    .chat-section {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1rem;
        margin: 1.5rem 0;
        border: 2px solid rgba(76, 175, 80, 0.5);
        box-shadow: 0 8px 32px rgba(76, 175, 80, 0.3);
        position: relative;
    }
    
    [data-theme="light"] .chat-section {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(33, 150, 243, 0.5);
        box-shadow: 0 8px 32px rgba(33, 150, 243, 0.2);
    }
    
    .chat-header {
        text-align: center;
        margin-bottom: 1rem;
        position: relative;
    }
    
    .chat-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: white;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    [data-theme="light"] .chat-title {
        color: #333;
    }
    
    .chat-subtitle {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
    }
    
    [data-theme="light"] .chat-subtitle {
        color: rgba(0, 0, 0, 0.6);
    }
    
    .processing-indicator {
        text-align: center;
        padding: 1rem;
        background: rgba(76, 175, 80, 0.2);
        border-radius: 12px;
        border: 1px solid rgba(76, 175, 80, 0.4);
        margin: 0.5rem 0;
    }
    
    [data-theme="light"] .processing-indicator {
        background: rgba(76, 175, 80, 0.1);
    }
    
    .success-message {
        color: #4caf50;
        font-weight: 600;
        font-size: 1rem;
    }
    
    /* Enhanced file uploader */
    .stFileUploader {
        margin-top: 0;
    }
    
    .stFileUploader > div {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
    }
    
    .stFileUploader > div > div {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
    }
    
    .stFileUploader > div > div > div {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 2px solid rgba(78, 205, 196, 0.6) !important;
        border-radius: 15px !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
        text-align: center !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    [data-theme="light"] .stFileUploader > div > div > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(33, 150, 243, 0.6) !important;
    }
    
    .stFileUploader > div > div > div:hover {
        border-color: #4ecdc4 !important;
        background: rgba(78, 205, 196, 0.1) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(78, 205, 196, 0.3) !important;
    }
    
    [data-theme="light"] .stFileUploader > div > div > div:hover {
        background: rgba(33, 150, 243, 0.05) !important;
        border-color: #2196f3 !important;
        box-shadow: 0 8px 25px rgba(33, 150, 243, 0.3) !important;
    }
    
    /* Upload button styling */
    .stFileUploader button {
        background: linear-gradient(45deg, #4ecdc4, #44a08d) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 23px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        margin-top: 1rem !important;
    }
    
    [data-theme="light"] .stFileUploader button {
        background: linear-gradient(45deg, #2196f3, #21cbf3) !important;
    }
    
    .stFileUploader button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(78, 205, 196, 0.4) !important;
    }
    
    [data-theme="light"] .stFileUploader button:hover {
        box-shadow: 0 8px 20px rgba(33, 150, 243, 0.4) !important;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 0.5rem 0;
    }
    
    [data-theme="light"] .stChatMessage {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    /* Enhanced sidebar */
    .css-1d391kg, .css-1cypcdb, .css-17lntkn {
        background: black !important;
        backdrop-filter: blur(10px) !important;
    }
    
    [data-theme="light"] .css-1d391kg,
    [data-theme="light"] .css-1cypcdb,
    [data-theme="light"] .css-17lntkn {
        background: rgba(255, 255, 255, 0.9) !important;
        border-right: 1px solid rgba(0, 0, 0, 0.1) !important;
    }
    
    /* MODIFIED: Feature Grid for 3 columns on all devices including mobile */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.8rem;
        margin: 1rem 0;
    }
    
    /* MODIFIED: Mobile responsive grid - maintains 3 columns even on small screens */
    @media (max-width: 768px) {
        .feature-grid {
            grid-template-columns: repeat(3, 1fr);
            gap: 0.8rem;
        }
    }
    
    /* MODIFIED: Feature cards with rectangular shape and proper radius */
    .feature-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 0.8rem 0.6rem; /* Reduced vertical padding for rectangular shape */
        border-radius: 12px; /* Consistent border radius */
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        min-height: 120px; /* Minimum height for consistency */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    [data-theme="light"] .feature-card {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    /* MODIFIED: Adjusted icon size for mobile */
    .feature-icon {
        font-size: 1.8rem; /* Slightly smaller for mobile */
        margin-bottom: 0.4rem;
    }
    
    /* MODIFIED: Responsive text sizing */
    .feature-title {
        font-weight: 700;
        color: white;
        margin-bottom: 0.3rem;
        font-size: 0.9rem; /* Slightly smaller for mobile */
    }
    
    [data-theme="light"] .feature-title {
        color: #333;
    }
    
    /* MODIFIED: Responsive description text */
    .feature-desc {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.75rem; /* Smaller for mobile readability */
        line-height: 1.2;
    }
    
    [data-theme="light"] .feature-desc {
        color: rgba(0, 0, 0, 0.6);
    }
    
    /* Additional mobile optimizations */
    @media (max-width: 480px) {
        .feature-icon {
            font-size: 1rem;
        }
        
        .feature-title {
            font-size: 0.8rem;
        }
        
        .feature-desc {
            font-size: 0.5rem;
        }
        
        .feature-card {
            padding: 0.7rem 0.4rem;
            min-height: 110px;
        }
    }
    
    /* Chat input enhancement */
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 0.5rem;
        margin-top: 1rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    [data-theme="light"] .stChatInputContainer {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(0, 0, 0, 0.1);
    }
    
    /* Pulse animation for chat section */
    @keyframes pulse {
        0% { box-shadow: 0 8px 32px rgba(76, 175, 80, 0.3); }
        50% { box-shadow: 0 8px 32px rgba(76, 175, 80, 0.5); }
        100% { box-shadow: 0 8px 32px rgba(76, 175, 80, 0.3); }
    }
    
    .chat-section {
        animation: pulse 2s infinite;
    }
    .[data-theme="light"] .sidebar{
        text-align: center; 
        padding: 1rem; 
        background: rgba(255,255,255,0.1); 
        border-radius: 10px; 
        margin-bottom: 1rem;
        color: black;
        }
    .[data-theme="dark"] .sidebar{
        text-align: center; 
        padding: 1rem; 
        background: rgba(255,255,255,0.1);
        border-radius: 10px; 
        margin-bottom: 1rem;
        color: white;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar with app info
    with st.sidebar:
        st.markdown("""
        <div class="sidebar">
            <h2 class="sidebar">📚 PDF Chat Assistant</h2>
            <p class="sidebar">Powered by AI</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        ### 🚀 How it works:
        1. **Upload** your PDF document
        2. **Wait** for processing to complete  
        3. **Ask** any questions about your document
        4. **Get** instant AI-powered answers
        """)
        
        st.markdown("---")
        
        st.markdown("""
        ### ✨ Features:
        - 🤖 **AI-Powered**: Advanced language understanding
        - ⚡ **Fast Search**: Vector-based document retrieval  
        - 💬 **Chat Interface**: Natural conversation flow
        - 📄 **PDF Support**: Extract text from any PDF
        """)
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <div class="main-title">Ask Your PDF 📝</div>
        <div class="subtitle">Transform any PDF into an interactive AI assistant</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Compact feature cards
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">Smart Analysis</div>
            <div class="feature-desc">AI understands context and provides accurate answers</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Lightning Fast</div>
            <div class="feature-desc">Get instant responses with advanced vector search</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">💼</div>
            <div class="feature-title">Professional</div>
            <div class="feature-desc">Perfect for research, work, and study materials</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced card-like file upload section
    upload_container = st.container()
    with upload_container:
    
        st.markdown("""
        <div class="upload-card-wrapper">
        <h2 style="color: white; margin-bottom: 0rem;text-align:center;">📁 Upload Your PDF Document</h2>
        </div>
        """, unsafe_allow_html=True)
        # File uploader with enhanced styling
        pdf = st.file_uploader(
            "Choose a PDF file",
            type='pdf',
            help="Upload your PDF document to start chatting with it",
            label_visibility="collapsed"
        )
    
    if pdf is not None:
        # Processing indicator
        with st.spinner('🔄 Processing your PDF...'):
            pdf_reader = PdfReader(pdf)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            # Split into chunks
            text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(text)
            
            # Better model for retrieval
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
            
            KNOWLEDGE_BASE = FAISS.from_texts(chunks, embeddings)
        
        # Success message and compact stats
        st.markdown("""
        <div class="processing-indicator">
            <div class="success-message">✅ PDF processed successfully!</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Compact document stats (only showing words)
        st.markdown(f"""
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-value">{len(text.split())}</div>
                <div class="stat-label">Words</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # PROMINENT CHAT SECTION
        st.markdown("""
        <div class="chat-section">
            <div class="chat-header">
                <div class="chat-title">
                    💬 Chat with your PDF
                </div>
                <div class="chat-subtitle">Ask any question about your document</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-lite", 
            google_api_key=GOOGLE_API_KEY, 
            temperature=0,
            max_retries=2,
        )
        
        # Chat container with messages
        chat_container = st.container()
        
        with chat_container:
            # Display chat messages
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
        
        # Prominent chat input
        user_question = st.chat_input("💭 Ask anything from your uploaded PDF...")
        
        if user_question:
            st.session_state.messages.append({"role": "user", "content": user_question})
            docs = KNOWLEDGE_BASE.similarity_search(user_question)
            chain = load_qa_chain(llm, chain_type="stuff")
            
            with st.chat_message("user"):
                st.write(user_question)
            
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                   
                    response = chain.run(input_documents=docs, question=user_question)
                    st.write(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Auto-scroll to bottom
            st.rerun()
    
    else:
        # Welcome message when no PDF is uploaded
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: rgba(255,255,255,0.7);">
            <h4>👆 Upload a PDF to get started</h4>
            <p>Once uploaded, you'll be able to ask questions and get instant answers from your document.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()