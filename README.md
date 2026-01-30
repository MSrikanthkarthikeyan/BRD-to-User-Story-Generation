# 🎯 BRD to User Story Generator

> **Enterprise AI-powered tool to transform Business Requirement Documents into production-ready Agile user stories**

[![Powered by Groq](https://img.shields.io/badge/Powered%20by-Groq%20AI-orange)](https://groq.com/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![BRD to User Story Generator](https://img.shields.io/badge/Status-Production%20Ready-success)

---

## ✨ Features

### 🚀 **6-Stage AI Processing Pipeline**
1. **📄 BRD Parsing & Analysis** - Analyzes document structure and completeness
2. **📋 Requirement Extraction** - Categorizes functional & non-functional requirements
3. **🎯 Context Synthesis** - Derives business context and user personas
4. **✍️ User Story Generation** - Creates Jira/Azure DevOps compatible stories
5. **✔️ QA & Validation** - Validates coverage and testability
6. **📦 Output Transformation** - Prepares multi-format exports

### 🎨 **Modern, Beautiful UI**
- Stunning gradient-based design with Embridge branding
- Dark blue sidebar with vibrant yellow accents
- Real-time progress tracking with visual indicators
- Interactive help system

### 📤 **Multi-Format Export**
- **PDF** - Executive-ready presentation format
- **Excel** - Jira/Azure DevOps importable spreadsheet
- **Word** - Comprehensive documentation
- **TXT** - Plain text for easy sharing

### ⚡ **Powered by Groq AI**
- **Blazing fast** inference with Llama 3.3 70B
- **Enterprise-grade** quality and accuracy
- **Generous free tier** (14,400 requests/day)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Groq API key ([Get one free](https://console.groq.com/))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/MSrikanthkarthikeyan/BRD-to-User-Story-Generation.git
cd BRD-to-User-Story-Generation
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API Key**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Groq API key
GROQ_API_KEY=your-groq-api-key-here
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open your browser**
- The app will automatically open at `http://localhost:8501`
- Upload your BRD document (PDF, DOCX, or TXT)
- Click "Start AI Processing"
- Download your user stories in your preferred format

---

## 📁 Project Structure

```
brd_to_userstory_generator/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── verify_setup.py            # Installation verification
│
├── modules/                   # Core processing modules
│   ├── __init__.py
│   ├── groq_service.py       # Groq API integration
│   ├── brd_parser.py         # BRD document parser
│   ├── requirement_extractor.py
│   ├── context_synthesizer.py
│   ├── story_generator.py
│   ├── qa_validator.py
│   ├── output_transformer.py
│   └── export_handlers.py    # Multi-format export
│
└── prompts/                   # AI prompt templates
    ├── task1_brd_parsing.txt
    ├── task2_extraction.txt
    ├── task3_synthesis.txt
    ├── task4_generation.txt
    ├── task5_validation.txt
    └── task6_transformation.txt
```

---

## 🎯 How It Works

### 1. **Upload Your BRD**
Upload your Business Requirement Document in PDF, DOCX, or TXT format.

### 2. **AI Processing**
The system processes your document through 6 intelligent stages:
- Analyzes document structure and quality
- Extracts and categorizes all requirements
- Synthesizes business context and user personas
- Generates enterprise-standard user stories
- Validates quality and coverage
- Prepares export-ready formats

### 3. **Review & Export**
- View detailed results for each processing stage
- Check summary metrics (stories, coverage, quality score)
- Download in your preferred format (PDF, Excel, Word, TXT)

---

## 🛠️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Groq API Configuration (Required)
GROQ_API_KEY=your-groq-api-key-here
GROQ_MODEL=llama-3.3-70b-versatile

# Optional: Customize settings
APP_NAME=BRD to User Story Generator
APP_BRAND=Embridge
```

### Getting a Groq API Key

1. Visit [console.groq.com](https://console.groq.com/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Generate a new API key
5. Copy and paste into your `.env` file

**Free Tier Limits:**
- 14,400 requests per day
- 30 requests per minute
- Perfect for production use

---

## 📊 Export Formats

### PDF Export
- Executive-ready presentation format
- Professional layout with Embridge branding
- Ideal for stakeholder reviews

### Excel Export
- **Jira/Azure DevOps compatible**
- Ready-to-import spreadsheet
- Structured columns for all story fields

### Word Export
- Comprehensive documentation format
- Detailed user stories with full context
- Perfect for detailed analysis

### TXT Export
- Plain text format
- Easy to share and edit
- Simple backup format

---

## 🎨 UI Features

### Stunning Modern Design
- **Vibrant gradients** - No transparency, solid professional colors
- **Modern typography** - Inter font family throughout
- **Smooth animations** - Button hovers, page transitions
- **Professional cards** - Elevated design with shadows
- **Color-coded metrics** - 🟢 Green, 🟡 Yellow, 🔴 Red quality indicators

### Real-Time Progress
- **6-stage pipeline visualization** - See exactly where processing is
- **Progress bar** - Visual feedback during processing
- **Status indicators** - ✅ Complete, 🔄 Processing, ⏳ Pending

### Interactive Help
- **Collapsible help section** - Quick guide always available
- **Tooltips** - Helpful hints on metrics and features
- **Error messages** - Clear guidance when issues occur

---

## 🔒 Security

### Best Practices
- ✅ API keys stored in `.env` file (not in code)
- ✅ `.env` file added to `.gitignore`
- ✅ No sensitive data committed to repository
- ✅ Secure API communication via HTTPS

### Data Privacy
- All processing happens via Groq's secure API
- No data is stored beyond the current session
- Uploaded files are temporarily stored and cleared on reset

---

## 🧪 Verification

Run the verification script to check your installation:

```bash
python verify_setup.py
```

This will check:
- ✅ Python version compatibility
- ✅ All required dependencies
- ✅ Project structure integrity
- ✅ Configuration status

---

## 📝 Sample Usage

```python
# Example: Processing a BRD programmatically
from modules.brd_parser import BRDParser
from modules.groq_service import GroqService

# Initialize parser
parser = BRDParser()

# Parse BRD
result = parser.parse_brd("path/to/your/brd.pdf")

# View analysis
print(f"Completeness Score: {result['completeness_score']}/100")
print(f"Sections Found: {len(result['sections_identified'])}")
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Groq AI** - For providing blazing-fast LLM inference
- **Streamlit** - For the amazing web app framework
- **Embridge** - Enterprise AI Solutions platform

---

## 📧 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/MSrikanthkarthikeyan/BRD-to-User-Story-Generation/issues)
- **Repository**: [github.com/MSrikanthkarthikeyan/BRD-to-User-Story-Generation](https://github.com/MSrikanthkarthikeyan/BRD-to-User-Story-Generation)

---

## 🚀 Roadmap

- [ ] Support for additional AI providers (Azure OpenAI, Anthropic)
- [ ] Batch processing for multiple BRDs
- [ ] Custom prompt template editor
- [ ] Integration with Jira/Azure DevOps APIs
- [ ] User story refinement and editing UI
- [ ] Template library for different industries

---

<div align="center">

**Made with ❤️ by the Embridge Team**

Powered by ⚡ [Groq AI](https://groq.com/) • Built with 🎈 [Streamlit](https://streamlit.io/)

</div>
