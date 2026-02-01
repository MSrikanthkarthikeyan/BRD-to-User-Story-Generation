# BRD to User Story Generator

Enterprise-grade AI-powered tool that transforms Business Requirements Documents (BRDs) into Agile user stories with acceptance criteria, built for Enbridge.

![Enbridge Logo](assets/enbridge_logo.png)

## 🎯 Overview

This application uses Azure OpenAI GPT-4o to automatically generate high-quality user stories from Business Requirements Documents in PDF, DOCX, or TXT format. It includes intelligent OCR for scanned documents and supports multiple export formats.

### Key Features

- **AI-Powered Generation**: Azure OpenAI GPT-4o for intelligent story creation
- **Smart OCR**: Automatic OCR for image-based/scanned PDFs using Groq Vision
- **Multi-Format Support**: Upload PDF, DOCX, TXT; export to PDF, Excel, Word, TXT
- **Quality Validation**: Built-in QA validation ensuring INVEST principles
- **Enterprise Design**: Professional Enbridge-branded interface

---

## 📋 Prerequisites

Before setting up this application, ensure you have:

1. **Python 3.11 or higher**
2. **Azure OpenAI Access**
   - Active Azure subscription
   - Azure OpenAI resource created
   - GPT-4o model deployed
3. **Groq API Key** (for OCR functionality)
4. **Git** installed

---

## 🚀 Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/MSrikanthkarthikeyan/BRD-to-User-Story-Generation.git
cd BRD-to-User-Story-Generation
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**What does requirements.txt do?**
- Lists all Python packages needed for the application
- Ensures everyone uses the same package versions
- Makes installation reproducible

**Key packages included:**
- `streamlit` - Web application framework
- `openai` - Azure OpenAI API client
- `groq` - Groq API for OCR
- `PyMuPDF` - PDF processing
- `python-docx` - Word document handling
- `openpyxl` - Excel export
- `reportlab` - PDF generation

### Step 4: Configure Environment Variables

**IMPORTANT: Why you don't see .env file in the repository**

The `.env` file contains sensitive API keys and secrets. For security:
- ✅ `.env` is listed in `.gitignore` → NOT pushed to GitHub
- ✅ `.env.example` is provided as a template → IS in the repository
- ✅ You must create your own `.env` file locally

**How to create your .env file:**

1. **Copy the template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env with your actual API keys:**
   ```bash
   notepad .env    # Windows
   nano .env       # Mac/Linux
   ```

3. **Fill in your credentials:**

   ```env
   # Azure OpenAI Configuration (Primary LLM)
   AZURE_OPENAI_KEY=your_actual_azure_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT=gpt-4o
   AZURE_OPENAI_MODEL=gpt-4o
   AZURE_OPENAI_API_VERSION=2024-08-01-preview

   # Groq API Configuration (OCR only)
   GROQ_API_KEY=your_actual_groq_key_here
   ```

### Step 5: Get Your API Keys

#### Azure OpenAI Key:
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Azure OpenAI resource
3. Go to "Keys and Endpoint"
4. Copy **Key 1** and **Endpoint**

#### Groq API Key:
1. Go to [Groq Console](https://console.groq.com)
2. Sign up/Login
3. Go to API Keys section
4. Create new API key

### Step 6: Verify Setup

```bash
python verify_setup.py
```

This script checks:
- ✅ All required packages installed
- ✅ `.env` file exists and is properly formatted
- ✅ API keys are configured
- ✅ Azure OpenAI connection works

### Step 7: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
BRD-to-User-Story-Generation/
│
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Files excluded from Git
├── verify_setup.py                 # Setup verification script
├── OCR_GUIDE.md                    # OCR troubleshooting guide
│
├── modules/                        # Core processing modules
│   ├── llm_service.py             # Azure OpenAI service
│   ├── groq_vision_ocr.py         # OCR for scanned PDFs
│   ├── brd_parser.py              # BRD document parser
│   ├── requirement_extractor.py   # Requirement extraction
│   ├── context_synthesizer.py     # Business context synthesis
│   ├── story_generator.py         # User story generation
│   ├── qa_validator.py            # Quality validation
│   ├── output_transformer.py      # Output formatting
│   └── export_handlers.py         # Export to PDF/Excel/Word/TXT
│
├── prompts/                        # LLM prompt templates
│   ├── task1_parsing.txt
│   ├── task2_extraction.txt
│   ├── task3_synthesis.txt
│   ├── task4_generation.txt
│   └── task5_validation.txt
│
└── assets/                         # Images and branding
    └── enbridge_logo.png
```

---

## 🔒 Security & Best Practices

### Why .gitignore is Critical

The `.gitignore` file tells Git which files to **never** commit to the repository:

```gitignore
# Never commit secrets
.env

# Don't commit temporary files
__pycache__/
*.log
temp/

# Don't commit output files
output/
*.pdf
*.xlsx
```

**Important:** If you accidentally commit `.env`:
```bash
git rm --cached .env
git commit -m "Remove .env from tracking"
git push
```

Then rotate (change) all your API keys immediately!

### API Key Management

- ✅ Store keys in `.env` file only
- ✅ Never share keys in emails/chat
- ✅ Rotate keys periodically
- ✅ Use separate keys for dev/prod
- ❌ Never hardcode keys in source code
- ❌ Never commit `.env` to Git

---

## 🎓 How to Use the Application

1. **Upload BRD**: Choose your PDF, DOCX, or TXT file
2. **Process**: Click "START AI PROCESSING"
3. **Review**: Check generated user stories in "View Results" tab
4. **Export**: Download in your preferred format (PDF/Excel/Word/TXT)

### Supported Input Formats
- **PDF**: Both text-based and scanned (OCR automatic)
- **DOCX**: Microsoft Word documents
- **TXT**: Plain text files

### Export Formats
- **PDF**: Executive presentation format
- **Excel**: Jira/Azure DevOps compatible
- **Word**: Comprehensive documentation
- **TXT**: Plain text format

---

## 🛠️ Troubleshooting

### "System Not Configured" Error
- ✅ Check `.env` file exists
- ✅ Verify API keys are correct
- ✅ Ensure no extra spaces in keys

### Import Errors
```bash
pip install -r requirements.txt --upgrade
```

### OCR Not Working
- See `OCR_GUIDE.md` for detailed troubleshooting
- Verify Groq API key is valid

### API Rate Limits
- Azure OpenAI has usage quotas
- Contact your Azure admin to increase limits

---

## 📊 Technical Details

### Architecture
- **Frontend**: Streamlit (Python)
- **LLM**: Azure OpenAI GPT-4o
- **OCR**: Groq Vision API
- **Export**: ReportLab (PDF), OpenPyXL (Excel), python-docx (Word)

### Processing Pipeline
1. **BRD Parsing** - Extract document structure
2. **Requirement Extraction** - Identify functional/non-functional requirements
3. **Context Synthesis** - Build business context
4. **Story Generation** - Generate user stories with acceptance criteria
5. **QA Validation** - Validate against INVEST principles
6. **Output Transformation** - Format for export

---

## 🤝 Support & Contact

For questions or issues:
- **Technical Issues**: Check `OCR_GUIDE.md` and troubleshooting section
- **API Access**: Contact your Azure/Groq administrator
- **Application Issues**: Review error messages and verify setup

---

## 📄 License

Developed for Enbridge. Internal use only.

---

**Ready to transform your BRDs into professional user stories! 🚀**
