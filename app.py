"""
BRD to User Story Generator - Streamlit Application
Enterprise tool with stunning Embridge branding
"""
import streamlit as st
import json
from pathlib import Path
import tempfile
import traceback

from config import Config
from modules.brd_parser import BRDParser
from modules.requirement_extractor import RequirementExtractor
from modules.context_synthesizer import ContextSynthesizer
from modules.story_generator import StoryGenerator
from modules.qa_validator import QAValidator
from modules.output_transformer import OutputTransformer
from modules.export_handlers import ExportHandler

# Page configuration
st.set_page_config(
    page_title=f"{Config.APP_NAME} | {Config.APP_BRAND}",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Enbridge-branded UI
st.markdown("""
<style>
   /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Main app background */
    .stApp {
        background: #ffffff;
    }
    
    
    /* Headers */
    h1 {
        color: #3D3D3D !important;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
    }
    
    h2 {
        color: #5A5A5A !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }
    
    h3 {
        color: #3D3D3D !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
    }
    
    /* Base text - dark and visible with hierarchy */
    p {
        color: #3D3D3D !important;
        line-height: 1.6 !important;
    }
    
    /* Secondary text - slightly lighter but still visible */
    .stMarkdown p {
        color: #3D3D3D !important;
    }
    
    /* Captions - darker for better visibility */
    .stCaptionContainer, [data-testid="stCaptionContainer"], .caption, [class*="caption"] {
        color: #495057 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    /* File uploader caption */
    [data-testid="stFileUploader"] + div {
        color: #495057 !important;
    }
    
    /* Text inputs */
    .stTextInput input, .stTextArea textarea {
        color: #3D3D3D !important;
        background: white !important;
    }
    
    /* Tab panel content */
    [data-baseweb="tab-panel"] {
        color: #3D3D3D !important;
    }
    
    /* Ensure list items are visible */
    li {
        color: #3D3D3D !important;
    }
    
    /* Strong/bold text */
    strong, b {
        color: #2A2A2A !important;
        font-weight: 700 !important;
    }
    
    /* Buttons - Enbridge orange */
    .stButton>button {
        background: linear-gradient(135deg, #F58220 0%, #E67817 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 15px rgba(245, 130, 32, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #E67817 0%, #D76E15 100%) !important;
        box-shadow: 0 6px 25px rgba(245, 130, 32, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    .stButton>button:active {
        transform: translateY(0px) !important;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: white !important;
        border: 2px dashed #F58220 !important;
        border-radius: 12px !important;
        padding: 2rem !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: #3D3D3D !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 1.5rem !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stFileUploader"] button:hover {
        background: #2A2A2A !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: #3D3D3D !important;
        font-weight: 600 !important;
    }
    
    /* Upload section - remove extra spacing */
    .upload-section {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Upload section */
    .upload-section {
        background: #ffffff !important;
        padding: 2.5rem !important;
        border-radius: 12px !important;
        border: 2px solid #F58220 !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 4px 20px rgba(245, 130, 32, 0.1) !important;
    }
    
    /* Stage card */
    .stage-card {
        background: linear-gradient(135deg, #FAFAFA 0%, #F5F5F5 100%) !important;
        padding: 2rem !important;
        border-radius: 12px !important;
        margin: 1rem 0 !important;
        border-left: 5px solid #F58220 !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08) !important;
        transition: all 0.3s ease !important;
    }
    
    .stage-card:hover {
        box-shadow: 0 5px 15px rgba(245, 130, 32, 0.15) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #2A2A2A !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-weight: 600 !important;
        color: #6c757d !important;
        font-size: 1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Messages */
    .stSuccess {
        background: #d4edda !important;
        border-left: 5px solid #28a745 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-weight: 600 !important;
        color: #155724 !important;
    }
    
    .stSuccess p, .stSuccess div {
        color: #155724 !important;
    }
    
    .stError {
        background: #f8d7da !important;
        border-left: 5px solid #dc3545 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-weight: 600 !important;
    }
    
    .stInfo {
        background: #FFF3E6 !important;
        border-left: 5px solid #F58220 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-weight: 600 !important;
        color: #3D3D3D !important;
    }
    
    /* Brand header */
    .brand-header {
        background: linear-gradient(135deg, #F58220 0%, #E67817 100%) !important;
        padding: 2rem !important;
        border-radius: 12px !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        box-shadow: 0 8px 30px rgba(245, 130, 32, 0.2) !important;
    }
    
    .brand-title {
        color: #ffffff !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2) !important;
    }
    
    .brand-subtitle {
        color: #ffffff !important;
        font-size: 1.2rem !important;
        margin-top: 0.5rem !important;
        font-weight: 500 !important;
        opacity: 0.95 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: transparent !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white !important;
        border-radius: 8px 8px 0 0 !important;
        color: #3D3D3D !important;
        font-weight: 600 !important;
        padding: 1rem 2rem !important;
        border: 2px solid #e0e0e0 !important;
        border-bottom: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #FFF3E6 !important;
        border-color: #F58220 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #F58220 0%, #E67817 100%) !important;
        color: #ffffff !important;
        border-color: #F58220 !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        color: #3D3D3D !important;
        padding: 1rem 1.5rem !important;
        border: 2px solid #dee2e6 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08) !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #FFF3E6 0%, #FFE8CC 100%) !important;
        border-color: #F58220 !important;
        box-shadow: 0 4px 8px rgba(245, 130, 32, 0.15) !important;
    }
    
    /* Hide expander arrow text completely - all methods */
    .streamlit-expanderHeader svg {
        color: #F58220 !important;
    }
    
    .streamlit-expanderHeader p {
        display: inline !important;
    }
    
    /* Hide arrow text using multiple methods */
    .streamlit-expanderHeader::before {
        content: none !important;
    }
    
    .streamlit-expanderHeader [data-testid="stMarkdownContainer"] p:first-child {
        font-size: 0 !important;
        line-height: 0 !important;
    }
    
    .streamlit-expanderHeader [data-testid="stMarkdownContainer"] {
        display: flex !important;
        align-items: center !important;
    }
    
    details summary::-webkit-details-marker {
        display: none !important;
    }
    
    details summary::marker {
        display: none !important;
    }
    
    /* Force hide any text content that looks like arrows */
    .streamlit-expanderHeader p:contains("arrow") {
        display: none !important;
    }
    
    /* Expander content */
    .streamlit-expanderContent {
        border: 2px solid #e9ecef !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        padding: 1.5rem !important;
        background: white !important;
    }
    
    /* Error expander styling */
    [data-testid="stExpander"] {
        background: transparent !important;
    }
    
    [data-testid="stExpander"] details summary {
        cursor: pointer !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #F58220 0%, #E67817 100%) !important;
    }
    
    /* Divider */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent 0%, #F58220 50%, transparent 100%) !important;
        margin: 2rem 0 !important;
    }
    
    /* Download button */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #3D3D3D 0%, #2A2A2A 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(61, 61, 61, 0.3) !important;
    }
    
    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #2A2A2A 0%, #1A1A1A 100%) !important;
        box-shadow: 0 6px 25px rgba(61, 61, 61, 0.5) !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #F58220 !important;
    }
    
    /* Block container */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Logo container */
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1rem 0;
        margin-bottom: 1rem;
    }
    
    .logo-container img {
        max-width: 200px;
        height: auto;
    }
    
    /* JSON and code display - prevent overflow */
    pre, code {
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        word-break: break-word !important;
        overflow-wrap: break-word !important;
        max-width: 100% !important;
        overflow-x: auto !important;
    }
    
    /* Expander content wrapping */
    .streamlit-expanderContent {
        overflow-x: auto !important;
        word-wrap: break-word !important;
    }
    
    /* JSON viewer styling */
    [data-testid="stJson"] {
        background: #f8f9fa !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        border: 1px solid #e9ecef !important;
        overflow-x: auto !important;
        max-width: 100% !important;
    }
    
    [data-testid="stJson"] pre {
        margin: 0 !important;
        white-space: pre-wrap !important;
        word-break: break-word !important;
    }
    
    /* Text areas and inputs */
    textarea, input {
        word-wrap: break-word !important;
    }
    
    /* Markdown content */
    .stMarkdown {
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    /* Prevent horizontal scroll on main container */
    .main .block-container {
        max-width: 100% !important;
        overflow-x: hidden !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = {}
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 0
if 'brd_text' not in st.session_state:
    st.session_state.brd_text = ""
if 'temp_file_path' not in st.session_state:
    st.session_state.temp_file_path = None

# Header with Enbridge logo
import base64
from pathlib import Path

# Load and encode logo
logo_path = Path(__file__).parent / "assets" / "enbridge_logo.png"
if logo_path.exists():
    with open(logo_path, "rb") as f:
        logo_data = base64.b64encode(f.read()).decode()
    logo_html = f'<div class="logo-container"><img src="data:image/png;base64,{logo_data}" alt="Enbridge Logo"></div>'
else:
    logo_html = ""

st.markdown(f"""
{logo_html}
<div class="brand-header">
    <h1 class="brand-title">{Config.APP_NAME}</h1>
</div>
""", unsafe_allow_html=True)

# Help and Actions section in main area
with st.expander("Help & Information", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### How to Use
        1. Upload BRD (PDF/DOCX/TXT)
        2. Click "START AI PROCESSING"
        3. Review generated stories
        4. Download your format
        
        **Powered by:**
        - **Azure OpenAI GPT-4o**
        - **Vision OCR** for scanned PDFs
        - Enbridge Platform
        
        **Scanned PDF Support:**
        Automatic OCR
        No installation required
        High accuracy extraction
        """)
    
    with col2:
        st.markdown("""
        ### What You Get
        - Enterprise Agile user stories
        - INVEST framework compliance
        - Acceptance criteria
        - Priority & risk analysis
        - Multiple export formats
        
        ### Supported Formats
        - **Upload**: PDF, DOCX, TXT
        - **Export**: PDF, Excel, Word, TXT
        """)

st.divider()

# Main content
tab1, tab2, tab3 = st.tabs(["Upload & Process", "View Results", "Export Files"])

with tab1:
    st.header("Upload Your BRD Document")
    st.markdown("Transform your Business Requirements into enterprise-grade Agile user stories with AI.")
    
    if not Config.is_configured():
        st.error("System Not Configured")
        st.markdown("""
        Azure Open AI API is required. Please configure in .env file.
        """)
        st.stop()
    else:
        # File upload
        st.markdown("### Step 1: Choose Your BRD File")
        uploaded_file = st.file_uploader(
            "Drag and drop or click to browse",
            type=['pdf', 'docx', 'txt'],
            help="Upload PDF, DOCX, or TXT format",
            label_visibility="collapsed"
        )
        st.markdown("<p style='color: #495057; font-size: 0.9rem; font-weight: 500; margin-top: 0.5rem;'>Supported: PDF, DOCX, TXT</p>", unsafe_allow_html=True)
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                st.session_state.temp_file_path = tmp_file.name
            
            st.markdown(f"<p style='color: #28a745; font-weight: 600; font-size: 1rem; margin: 1rem 0;'>✓ {uploaded_file.name} is ready for processing</p>", unsafe_allow_html=True)
            
            st.markdown("### Step 2: Start AI Processing")
            
            # Process button
            if st.button("START AI PROCESSING", type="primary", use_container_width=True):
                try:
                    st.info("Smart OCR: Image-based PDFs automatically processed with Vision OCR - no installation needed!")
                    
                    # Initialize modules
                    brd_parser = BRDParser()
                    req_extractor = RequirementExtractor()
                    context_synth = ContextSynthesizer()
                    story_gen = StoryGenerator()
                    qa_validator = QAValidator()
                    output_transformer = OutputTransformer()
                    
                    # Progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Stage 1: BRD Parsing
                    status_text.markdown("### Stage 1/6: Analyzing BRD Structure...")
                    progress_bar.progress(1/6)
                    st.session_state.current_stage = 1
                    
                    parsing_result = brd_parser.parse_brd(st.session_state.temp_file_path)
                    st.session_state.processed_data['parsing'] = parsing_result
                    
                    # Extract and store BRD text
                    st.session_state.brd_text = brd_parser.extract_text_from_file(st.session_state.temp_file_path)
                    
                    # DEBUG: Print first 500 chars to verify OCR content
                    print("=" * 80)
                    print("DEBUG: BRD TEXT EXTRACTED")
                    print(f"Total length: {len(st.session_state.brd_text)} characters")
                    print(f"First 500 characters:")
                    print(st.session_state.brd_text[:500])
                    print("=" * 80)
                    
                    # Stage 2: Requirement Extraction
                    status_text.markdown("### Stage 2/6: Extracting Requirements...")
                    progress_bar.progress(2/6)
                    st.session_state.current_stage = 2
                    
                    requirements = req_extractor.extract_requirements(
                        st.session_state.brd_text,
                        parsing_result
                    )
                    st.session_state.processed_data['requirements'] = requirements
                    
                    # DEBUG: Print requirement extraction results
                    print("=" * 80)
                    print("DEBUG: REQUIREMENTS EXTRACTED")
                    print(f"Functional requirements: {len(requirements.get('functional_requirements', []))}")
                    print(f"Non-functional requirements: {len(requirements.get('non_functional_requirements', []))}")
                    if requirements.get('functional_requirements'):
                        print("First functional requirement:")
                        print(json.dumps(requirements['functional_requirements'][0], indent=2))
                    print("=" * 80)
                    
                    # Stage 3: Context Synthesis
                    status_text.markdown("### Stage 3/6: Synthesizing Business Context...")
                    progress_bar.progress(3/6)
                    st.session_state.current_stage = 3
                    
                    context = context_synth.synthesize_context(requirements)
                    st.session_state.processed_data['context'] = context
                    
                    # Stage 4: User Story Generation
                    status_text.markdown("### Stage 4/6: Generating User Stories...")
                    progress_bar.progress(4/6)
                    st.session_state.current_stage = 4
                    
                    stories = story_gen.generate_stories(requirements, context)
                    st.session_state.processed_data['stories'] = stories
                    
                    # Stage 5: QA Validation
                    status_text.markdown("### Stage 5/6: Validating Quality...")
                    progress_bar.progress(5/6)
                    st.session_state.current_stage = 5
                    
                    validation = qa_validator.validate_stories(requirements, stories)
                    st.session_state.processed_data['validation'] = validation
                    
                    # Stage 6: Output Transformation
                    status_text.markdown("### Stage 6/6: Preparing Exports...")
                    progress_bar.progress(6/6)
                    st.session_state.current_stage = 6
                    
                    output = output_transformer.transform_for_export(stories, context)
                    st.session_state.processed_data['output'] = output
                    
                    # Complete
                    progress_bar.progress(1.0)
                    status_text.markdown("### Processing Complete")
                    st.session_state.current_stage = 7
                    
                    st.balloons()
                    st.success("Success! User stories generated. Check the results tab!")
                    
                except Exception as e:
                    st.error(f"Processing Error: {str(e)}")
                    st.markdown("""
                    <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 1rem; border-radius: 4px; margin-top: 1rem;">
                        <p style="color: #856404; margin: 0; font-weight: 600;">⚠️ Troubleshooting Tips:</p>
                        <ul style="color: #856404; margin-top: 0.5rem; margin-bottom: 0;">
                            <li>Verify Azure OpenAI credentials in .env file</li>
                            <li>Check API endpoint and deployment name</li>
                            <li>Ensure active subscription and valid API key</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

with tab2:
    st.header("Processing Results & Analysis")
    
    if not st.session_state.processed_data:
        st.info("Upload and process a BRD document first")
        st.markdown("""
        Once complete, you'll see:
        - Summary metrics and quality scores
        - Stage-by-stage analysis results 
        - Generated user stories with traceability
        """)
    else:
        # Summary metrics first
        if 'stories' in st.session_state.processed_data:
            st.subheader("Key Metrics")
            
            stories_data = st.session_state.processed_data['stories']
            validation_data = st.session_state.processed_data.get('validation', {})
            
            # Metrics row
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="User Stories",
                    value=len(stories_data.get('user_stories', [])),
                    help="Total generated user stories"
                )
            
            with col2:
                st.metric(
                    label="Epic Groups",
                    value=len(stories_data.get('epic_groupings', [])),
                    help="Feature groupings"
                )
            
            with col3:
                coverage = validation_data.get('coverage_analysis', {}).get('coverage_percentage', 0)
                st.metric(
                    label="Coverage",
                    value=f"{coverage:.0f}%",
                    help="BRD requirements covered"
                )
            
            with col4:
                quality = validation_data.get('overall_quality_score', 0)
                color = "🟢" if quality >= 80 else "🟡" if quality >= 60 else "🔴"
                st.metric(
                    label="Quality Score",
                    value=f"{color} {quality}/100",
                    help="Overall quality rating"
                )
            
            st.divider()
        
        # Stage results
        st.subheader("📌 Detailed Stage Results")
        
        stage_names = {
            'parsing': '🔍 BRD Parsing & Analysis',
            'requirements': '📋 Requirements Extraction',
            'context': '🎯 Business Context Synthesis',
            'stories': '✍️ User Stories Generated',
            'validation': '✔️ QA Validation Results'
        }
        
        for stage_key, stage_title in stage_names.items():
            if stage_key in st.session_state.processed_data:
                with st.expander(stage_title, expanded=(stage_key == 'stories')):
                    stage_data = st.session_state.processed_data[stage_key]
                    
                    # Show key highlights
                    if stage_key == 'parsing':
                        completeness = stage_data.get('completeness_score', 0)
                        st.markdown(f"**Completeness Score:** {completeness}/100")
                    elif stage_key == 'requirements':
                        fr_count = len(stage_data.get('functional_requirements', []))
                        nfr_count = len(stage_data.get('non_functional_requirements', []))
                        st.markdown(f"**Functional:** {fr_count} | **Non-Functional:** {nfr_count}")
                        
                        # Display requirements in a readable format
                        if fr_count > 0:
                            st.markdown("#### Functional Requirements")
                            for req in stage_data.get('functional_requirements', [])[:5]:  # Show first 5
                                with st.container():
                                    st.markdown(f"""
                                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid #F58220;">
                                        <strong>{req.get('requirement_id', 'N/A')}</strong> - {req.get('category', 'General')}<br/>
                                        <span style="color: #5A5A5A;">{req.get('description', 'N/A')}</span><br/>
                                        <small style="color: #6c757d;">Priority: {req.get('priority', 'N/A')} | Confidence: {req.get('confidence', 'N/A')}</small>
                                    </div>
                                    """, unsafe_allow_html=True)
                            if fr_count > 5:
                                st.caption(f"+ {fr_count - 5} more functional requirements")
                    
                    elif stage_key == 'context':
                        personas = len(stage_data.get('user_personas', []))
                        st.markdown(f"**User Personas:** {personas}")
                    
                    elif stage_key == 'stories':
                        stories_count = len(stage_data.get('user_stories', []))
                        st.markdown(f"**Total Stories:** {stories_count}")
                        
                        # Display user stories in a card format
                        if stories_count > 0:
                            st.markdown("---")
                            for idx, story in enumerate(stage_data.get('user_stories', [])[:3], 1):  # Show first 3
                                st.markdown(f"""
                                <div style="background: white; padding: 1.5rem; border-radius: 12px; margin: 1rem 0; border: 2px solid #e9ecef; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                                        <h4 style="margin: 0; color: #3D3D3D; font-size: 1.1rem;">{story.get('story_id', f'US-{idx}')} - {story.get('title', 'Untitled')}</h4>
                                        <span style="background: #FFF3E6; color: #F58220; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.85rem; font-weight: 600;">{story.get('priority', 'Medium')}</span>
                                    </div>
                                    <p style="color: #5A5A5A; font-size: 1rem; line-height: 1.6; margin: 0.5rem 0; font-style: italic;">
                                        "{story.get('user_story', 'N/A')}"
                                    </p>
                                    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #e9ecef;">
                                        <strong style="color: #3D3D3D; font-size: 0.9rem;">Epic:</strong> <span style="color: #6c757d;">{story.get('epic', 'General')}</span> | 
                                        <strong style="color: #3D3D3D; font-size: 0.9rem;">Feature:</strong> <span style="color: #6c757d;">{story.get('feature', 'N/A')}</span>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            if stories_count > 3:
                                st.caption(f"+ {stories_count - 3} more user stories (view in Export)")
                    
                    elif stage_key == 'validation':
                        issues = len(stage_data.get('ambiguity_issues', [])) + len(stage_data.get('testability_issues', []))
                        st.markdown(f"**Issues Flagged:** {issues}")

with tab3:
    st.header("Export User Stories")
    
    if 'output' not in st.session_state.processed_data:
        st.info("Complete processing first")
        st.markdown("""
        After processing, download in multiple formats:
        - PDF – Executive presentation
        - Excel – Jira/Azure DevOps import
        - **Word** – Full documentation
        - **TXT** – Plain text
        """)
    else:
        st.success("Your user stories are ready to download!")
        st.markdown("Choose your preferred format:")
        
        export_handler = ExportHandler()
        output_structure = st.session_state.processed_data['output']
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Pre-generate all exports with caching
        if 'export_files' not in st.session_state:
            with st.spinner("Preparing export files..."):
                try:
                    st.session_state.export_files = {}
                    st.session_state.export_files['pdf'] = export_handler.export_to_pdf(output_structure)
                    st.session_state.export_files['excel'] = export_handler.export_to_excel(output_structure)
                    st.session_state.export_files['word'] = export_handler.export_to_word(output_structure)
                    st.session_state.export_files['txt'] = export_handler.export_to_txt(output_structure)
                except Exception as e:
                    st.error(f"Error generating exports: {str(e)}")
                    st.stop()
        
        # Export grid with single-click downloads
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### PDF Export")
            st.caption("Executive-ready presentation")
            with open(st.session_state.export_files['pdf'], 'rb') as f:
                st.download_button(
                    label="DOWNLOAD PDF",
                    data=f.read(),
                    file_name=Path(st.session_state.export_files['pdf']).name,
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("### Word Export")
            st.caption("Comprehensive documentation")
            with open(st.session_state.export_files['word'], 'rb') as f:
                st.download_button(
                    label="DOWNLOAD WORD",
                    data=f.read(),
                    file_name=Path(st.session_state.export_files['word']).name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                    type="primary"
                )
        
        with col2:
            st.markdown("### Excel Export")
            st.caption("Jira/DevOps compatible")
            with open(st.session_state.export_files['excel'], 'rb') as f:
                st.download_button(
                    label="DOWNLOAD EXCEL",
                    data=f.read(),
                    file_name=Path(st.session_state.export_files['excel']).name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    type="primary"
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("### TXT Export")
            st.caption("Plain text format")
            with open(st.session_state.export_files['txt'], 'r', encoding='utf-8') as f:
                st.download_button(
                    label="DOWNLOAD TXT",
                    data=f.read(),
                    file_name=Path(st.session_state.export_files['txt']).name,
                    mime="text/plain",
                    use_container_width=True,
                    type="primary"
                )

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 2rem 0;">
    <p style="margin: 0; font-size: 1rem; font-weight: 600;">
        <span style="color: #F58220;">Enbridge</span> GenAI Solutions
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #6c757d;">
        Powered by Azure OpenAI GPT-4o
    </p>
</div>
""", unsafe_allow_html=True)
