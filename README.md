# 📚 PDF Chat Assistant

An intelligent AI-powered application that transforms your PDF documents into interactive chat experiences. Upload any PDF and start having conversations with your documents using advanced language models and vector search technology.

## ✨ Features

- 🤖 **AI-Powered Conversations**: Chat naturally with your PDF documents using Google's Gemini 2.0 Flash Lite
- ⚡ **Lightning Fast Search**: Vector-based document retrieval with FAISS for instant responses
- 💬 **Streaming Responses**: Real-time response generation for better user experience
- 📱 **Responsive Design**: Beautiful, mobile-friendly interface that works on all devices
- 🎨 **Modern UI**: Glassmorphism design with dynamic backgrounds and smooth animations
- 📄 **Smart Text Processing**: Intelligent text chunking and embedding for optimal performance
- 🔍 **Context-Aware**: Maintains conversation context for more accurate responses

## 🚀 Demo

### Key Capabilities:
- **Document Analysis**: Upload PDFs and get instant insights
- **Question Answering**: Ask specific questions about document content
- **Research Assistant**: Perfect for academic papers, reports, and manuals

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Google API Key for Gemini

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/pdf-chat-assistant.git
cd pdf-chat-assistant
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📦 Dependencies

```txt
streamlit>=1.28.0
PyPDF2>=3.0.1
langchain>=0.0.350
langchain-google-genai>=1.0.0
faiss-cpu>=1.7.4
sentence-transformers>=2.2.2
python-dotenv>=1.0.0
```

## 🔧 Configuration


### Model Configuration
The app uses Google's Gemini 2.0 Flash Lite model by default. You can modify the model in the code:


## 📱 Usage

### Basic Workflow:
1. **Upload PDF**: Click the upload area and select your PDF document
2. **Wait for Processing**: The app will extract and process the text
3. **Start Chatting**: Ask questions about your document in natural language
4. **Get Instant Answers**: Receive AI-powered responses with context

### Example Questions:
- "What is the main topic of this document?"
- "Summarize the key findings in chapter 3"
- "What are the recommendations mentioned?"
- "Explain the methodology used in this research"

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   PDF Upload    │───▶│  Text Extraction │───▶│ Text Chunking   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ User Interface  │◀───│   Chat Handler   │◀───│ Vector Store    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │               ┌──────────────────┐    ┌─────────────────┐
         └──────────────▶│ Gemini 2.0 Flash │◀───│   Embeddings    │
                         └──────────────────┘    └─────────────────┘
```

### Key Components:
- **PyPDF2**: PDF text extraction
- **LangChain**: Text processing and chain management
- **FAISS**: Vector similarity search
- **Sentence Transformers**: Text embeddings
- **Streamlit**: Web interface
- **Google Gemini**: Language model

## 🎨 UI Features

- **Glassmorphism Design**: Modern translucent card-based interface
- **Dark/Light Mode**: Automatically adapts to system theme
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile
- **Real-time Streaming**: See responses generate in real-time
- **Interactive Animations**: Smooth hover effects and transitions
- **Progress Indicators**: Visual feedback during processing

## 🔒 Privacy & Security

- **Local Processing**: Documents are processed locally on your machine
- **No Data Storage**: No documents or conversations are permanently stored
- **API Security**: Secure communication with Google's API
- **Session-based**: All data is cleared when you close the application

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Setup:
```bash
git clone https://github.com/yourusername/pdf-chat-assistant.git
cd ragbot
pip install -r requirements-dev.txt
```

### Contribution Guidelines:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Contribution:
- 📝 Additional document format support (DOCX, TXT, etc.)
- 🌐 Multi-language support
- 🔍 Advanced search features
- 📊 Document analytics and insights
- 🎨 UI/UX improvements

## 🐛 Troubleshooting

### Common Issues:

**Issue**: "Google API Key not found"
```bash
Solution: Ensure your .env file contains GOOGLE_API_KEY=your_key_here
```

**Issue**: "Failed to process PDF"
```bash
Solution: Check if PDF is text-based (not scanned images)
```

**Issue**: "Streaming not working"
```bash
Solution: Check internet connection and API limits
```

**Issue**: "Module not found"
```bash
Solution: Run pip install -r requirements.txt
```

## 📈 Performance Tips

- **Optimal PDF Size**: Best performance with PDFs under 50MB
- **Text Quality**: Works best with text-based PDFs (not scanned documents)
- **Question Specificity**: More specific questions yield better results
- **Internet Connection**: Stable connection required for API calls

## 🔄 Updates & Changelog

### Version 1.0.0 (Current)
- Initial release with core functionality
- Google Gemini 2.0 Flash Lite integration
- Responsive UI with glassmorphism design
- Real-time streaming responses
- Mobile-optimized interface

### Planned Features:
- [ ] Multiple PDF support
- [ ] Document comparison
- [ ] Export chat history
- [ ] Advanced filtering options
- [ ] OCR for scanned documents

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google AI**: For providing the Gemini API
- **LangChain**: For the excellent framework
- **Streamlit**: For the amazing web app framework
- **Hugging Face**: For the embedding models
- **FAISS**: For efficient similarity search



## ⭐ Show Your Support

If you found this project helpful, please give it a ⭐ on GitHub!

 