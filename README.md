# BRD to User Story Generator

> **Enterprise AI Solution by Embridge**  
> Convert Business Requirement Documents into Agile user stories using Azure OpenAI

![Version](https://img.shields.io/badge/version-1.0.0-yellow)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 Overview

An enterprise-grade Streamlit application that transforms Business Requirement Documents (BRDs) into comprehensive, Jira/Azure DevOps-compatible user stories using Azure OpenAI's advanced AI capabilities.

### Key Features

- **6-Stage AI Processing Pipeline**
  - BRD Parsing & Analysis
  - Requirement Extraction with Traceability
  - Business Context Synthesis
  - User Story Generation
  - QA & Coverage Validation
  - Multi-Format Output Transformation

- **Multi-Format Export**
  - PDF (Executive-ready format)
  - Excel (Jira/Azure DevOps importable)
  - Word (Documentation style)
  - Plain Text

- **Enterprise Branding**
  - Embridge white & yellow theme
  - Professional UI/UX
  - Real-time progress tracking
  - Comprehensive error handling

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Azure OpenAI API access
- Azure OpenAI deployment (GPT-4 recommended)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd d:\antigravity-projects\brd_to_userstory_generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Azure OpenAI**
   
   Copy the example environment file:
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` and add your Azure OpenAI credentials:
   ```env
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key-here
   AZURE_OPENAI_DEPLOYMENT=gpt-4
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

The application will open in your browser at `http://localhost:8501`

---

## 📖 Usage Guide

### Step-by-Step Workflow

1. **Upload BRD Document**
   - Supported formats: PDF, DOCX, TXT
   - Click "Browse files" in the Upload tab
   - Select your Business Requirement Document

2. **Start Processing**
   - Click "🚀 Start Processing" button
   - Monitor real-time progress through 6 stages:
     1. BRD Parsing - Document structure analysis
     2. Requirement Extraction - Categorized requirements with traceability
     3. Context Synthesis - Business context and user personas
     4. User Story Generation - Enterprise Agile user stories
     5. QA Validation - Coverage and quality checks
     6. Output Transformation - Format-ready structures

3. **Review Results**
   - Navigate to "Results" tab
   - Expand each stage to view JSON outputs
   - Check summary metrics (stories count, coverage, quality score)

4. **Export User Stories**
   - Navigate to "Export" tab
   - Choose your desired format:
     - **PDF** - Executive presentation format
     - **Excel** - Import directly into Jira/Azure DevOps
     - **Word** - Comprehensive documentation
     - **TXT** - Plain text for easy sharing

---

## 🏗️ Architecture

### Project Structure

```
brd_to_userstory_generator/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── README.md                  # This file
├── modules/
│   ├── __init__.py
│   ├── brd_parser.py          # Task 1: BRD parsing
│   ├── requirement_extractor.py # Task 2: Requirement extraction
│   ├── context_synthesizer.py  # Task 3: Context synthesis
│   ├── story_generator.py      # Task 4: User story generation
│   ├── qa_validator.py         # Task 5: QA validation
│   ├── output_transformer.py   # Task 6: Output transformation
│   ├── openai_service.py       # Azure OpenAI integration
│   └── export_handlers.py      # Export functionality
├── prompts/
│   ├── task1_brd_parsing.txt
│   ├── task2_extraction.txt
│   ├── task3_synthesis.txt
│   ├── task4_generation.txt
│   ├── task5_validation.txt
│   └── task6_transformation.txt
├── assets/                     # Brand assets
└── exports/                    # Generated output files
```

### Processing Pipeline

```
BRD Upload → Parsing → Extraction → Synthesis → Generation → Validation → Export
    ↓           ↓          ↓            ↓            ↓            ↓          ↓
  File       Structure  Requirements  Context    User Stories   QA Check  PDF/Excel/
  Input      Analysis   Categorized   Derived    Generated      Coverage  Word/TXT
```

---

## 🔧 Configuration

### Azure OpenAI Settings

Edit `.env` file or configure via the Streamlit sidebar:

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI resource endpoint | `https://your-resource.openai.azure.com/` |
| `AZURE_OPENAI_API_KEY` | API key for authentication | `your-api-key-here` |
| `AZURE_OPENAI_DEPLOYMENT` | Model deployment name | `gpt-4` or `gpt-4-turbo` |
| `AZURE_OPENAI_API_VERSION` | API version | `2024-02-15-preview` |

### Model Recommendations

- **GPT-4**: Best quality, comprehensive analysis
- **GPT-4-Turbo**: Faster processing, good quality
- **GPT-3.5-Turbo**: Budget option, basic analysis

---

## 📊 Export Formats

### PDF Export
- Executive-ready presentation format
- Organized by epics and user stories
- Includes traceability matrix
- Embridge branding (yellow highlights)

### Excel Export (Jira-Compatible)
- Flat table structure
- Headers: Story ID, Title, User Role, Description, Acceptance Criteria, Priority, Story Points, Status, Dependencies, Epic, BRD Reference
- Ready for CSV/Excel import into Jira or Azure DevOps
- Embridge header styling

### Word Export
- Professional documentation format
- Hierarchical structure (Epics → Stories)
- Tables for traceability matrix
- Suitable for stakeholder review

### TXT Export
- Plain text format
- Easy to share via email or chat
- Human-readable structure
- No special software required

---

## 🛠️ Troubleshooting

### Common Issues

**Issue: "Missing configuration" error**
- **Solution**: Ensure `.env` file is properly configured with all required Azure OpenAI credentials

**Issue: API call failures**
- **Solution**: Verify API key is valid and deployment name matches your Azure resource

**Issue: File upload errors**
- **Solution**: Ensure file is in supported format (PDF, DOCX, TXT) and not corrupted

**Issue: Export button not working**
- **Solution**: Complete all processing stages before attempting export

**Issue: Slow processing**
- **Solution**: Large documents may take several minutes. GPT-4-Turbo is faster than GPT-4

---

## 📝 Best Practices

### For Best Results

1. **BRD Quality**
   - Use well-structured BRDs with clear sections
   - Include explicit functional and non-functional requirements
   - Define stakeholders and success criteria

2. **Model Selection**
   - Use GPT-4 for complex, critical projects
   - Use GPT-4-Turbo for faster turnaround
   - Lower temperature (0.2-0.3) for analytical tasks

3. **Review Process**
   - Always review generated user stories
   - Check acceptance criteria for testability
   - Verify traceability to BRD requirements

4. **Export Strategy**
   - Use Excel for Jira/Azure DevOps import
   - Use PDF for stakeholder presentations
   - Use Word for detailed documentation
   - Use TXT for quick sharing

---

## 🔐 Security Notes

- Never commit `.env` file to version control
- Rotate API keys regularly
- Use Azure RBAC for access control
- Review generated content before external sharing

---

## 🤝 Support

For issues, questions, or feature requests:
- Contact: Embridge AI Solutions Team
- Documentation: See implementation plan in `brain/` directory

---

## 📄 License

Copyright © 2026 Embridge. All rights reserved.

---

## 🎨 Embridge Branding

The application features Embridge's signature white & yellow theme:
- **Primary Color**: Yellow (`#FFD700`)
- **Background**: White (`#FFFFFF`)
- **Text**: Dark Gray (`#1F1F1F`)
- **Accent**: Light Yellow (`#FFFEF0`)

---

**Built with ❤️ by Embridge AI Solutions**
