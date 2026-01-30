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
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for stunning, modern UI with solid colors
st.markdown("""
<style>
   /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Main app background - solid white */
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #fffef9 100%);
    }
    
    /* Sidebar - solid vibrant gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFD700 !important;
        font-weight: 700 !important;
    }
    
    /* Headers - bold and vibrant */
    h1 {
        color: #1a1a2e !important;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
    }
    
    h2 {
        color: #16213e !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }
    
    h3 {
        color: #0f3460 !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
    }
    
    /* Buttons - vibrant yellow with modern effects */
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #FFC700 100%) !important;
        color: #1a1a2e !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #FFC700 0%, #FFB700 100%) !important;
        box-shadow: 0 6px 25px rgba(255, 215, 0, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    .stButton>button:active {
        transform: translateY(0px) !important;
    }
    
    /* File uploader - modern card style */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #fff9e6 0%, #fffef5 100%) !important;
        border: 3px dashed #FFD700 !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
    }
    
    /* Upload section styling */
    .upload-section {
        background: linear-gradient(135deg, #ffffff 0%, #fff9e6 100%) !important;
        padding: 2.5rem !important;
        border-radius: 20px !important;
        border: 2px solid #FFD700 !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 8px 30px rgba(255, 215, 0, 0.15) !important;
    }
    
    /* Stage card  */
    .stage-card {
        background: linear-gradient(135deg, #ffffff 0%, #fffef5 100%) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        margin: 1rem 0 !important;
        border-left: 5px solid #FFD700 !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #1a1a2e !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-weight: 600 !important;
        color: #16213e !important;
        font-size: 1rem !important;
    }
    
    /* Success/Error/Info messages */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%) !important;
        border-left: 5px solid #28a745 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-weight: 600 !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%) !important;
        border-left: 5px solid #dc3545 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-weight: 600 !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%) !important;
        border-left: 5px solid #17a2b8 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-weight: 600 !important;
    }
    
    /* Brand header - vibrant gradient */
    .brand-header {
        background: linear-gradient(135deg, #FFD700 0%, #FFC700 50%, #FFB700 100%) !important;
        padding: 3rem 2rem !important;
        border-radius: 20px !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        box-shadow: 0 10px 40px rgba(255, 215, 0, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .brand-header::before {
        content: '' !important;
        position: absolute !important;
        top: -50% !important;
        left: -50% !important;
        width: 200% !important;
        height: 200% !important;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%) !important;
        animation: pulse 4s ease-in-out infinite !important;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .brand-title {
        color: #1a1a2e !important;
        font-size: 3rem !important;
        font-weight: 900 !important;
        margin: 0 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1) !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    .brand-subtitle {
        color: #16213e !important;
        font-size: 1.3rem !important;
        margin-top: 0.5rem !important;
        font-weight: 600 !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    /* Tabs - modern design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: transparent !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white !important;
        border-radius: 12px 12px 0 0 !important;
        color: #16213e !important;
        font-weight: 600 !important;
        padding: 1rem 2rem !important;
        border: 2px solid transparent !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #fff9e6 !important;
        border-color: #FFD700 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FFD700 0%, #FFC700 100%) !important;
        color: #1a1a2e !important;
        border-color: #FFD700 !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%) !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        color: #1a1a2e !important;
        padding: 1rem !important;
        border: 2px solid #e9ecef !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #fffef5 0%, #fff9e6 100%) !important;
        border-color: #FFD700 !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #FFD700 0%, #FFC700 100%) !important;
    }
    
    /* Divider */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent 0%, #FFD700 50%, transparent 100%) !important;
        margin: 2rem 0 !important;
    }
    
    /* Download button */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.4) !important;
    }
    
    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #20c997 0%, #17a2b8 100%) !important;
        box-shadow: 0 6px 25px rgba(40, 167, 69, 0.6) !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #FFD700 !important;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Caption text */
    .caption {
        color: #6c757d !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
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

# Header
st.markdown(f"""
<div class="brand-header">
    <h1 class="brand-title">🎯 {Config.APP_NAME}</h1>
    <p class="brand-subtitle">Powered by {Config.APP_BRAND} | Enterprise AI Solutions</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Modern solid design
with st.sidebar:
    # Branding
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0;">
        <h2 style="margin: 0;">🎯 Embridge</h2>
        <p style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">Enterprise AI Solutions</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Configuration Status (minimal, no exposure)
    if Config.is_configured():
        st.success("✅ **System Ready**")
        st.caption("Groq AI Configured (Llama 3.3 70B)")
    else:
        st.error("⚠️ **Configuration Required**")
        st.info("Please configure Groq API key in environment")
    
    st.divider()
    
    # Processing Pipeline
    st.subheader("📊 Processing Pipeline")
    stages = [
        ("📤", "Upload"),
        ("🔍", "Parsing"),
        ("📋", "Extraction"),
        ("🎯", "Synthesis"),
        ("✍️", "Generation"),
        ("✔️", "Validation"),
        ("📦", "Complete")
    ]
    
    for idx, (icon, stage) in enumerate(stages):
        if idx < st.session_state.current_stage:
            st.markdown(f"<div style='color: #28a745; font-weight: 600;'>{icon} {stage} ✅</div>", unsafe_allow_html=True)
        elif idx == st.session_state.current_stage:
            st.markdown(f"<div style='color: #FFD700; font-weight: 700;'>{icon} {stage} 🔄</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='opacity: 0.6;'>{icon} {stage}</div>", unsafe_allow_html=True)
    
    st.divider()
    
    # Actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.processed_data = {}
            st.session_state.current_stage = 0
            st.session_state.brd_text = ""
            st.session_state.temp_file_path = None
            st.rerun()
    
    with col2:
        if st.button("ℹ️ Help", use_container_width=True):
            st.session_state['show_help'] = not st.session_state.get('show_help', False)
    
    # Help section
    if st.session_state.get('show_help', False):
        st.divider()
        st.markdown("""
        **Quick Guide:**
        1. Upload your BRD (PDF/DOCX/TXT)
        2. Click "Start Processing"
        3. Review AI-generated results
        4. Download your format
        
        **Powered by:**
        - Groq AI (Llama 3.3 70B)
        - Embridge Platform
        """)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; opacity: 0.8;">
        <p style="font-size: 0.75rem; margin: 0;">v1.0.0</p>
    </div>
    """, unsafe_allow_html=True)

# Main content
tab1, tab2, tab3 = st.tabs(["📤 Upload & Process", "📋 View Results", "📥 Export Files"])

with tab1:
    st.header("Upload Your BRD Document")
    st.markdown("Transform your Business Requirements into enterprise-grade Agile user stories with AI.")
    
    if not Config.is_configured():
        st.error("🔒 **System Not Configured**")
        st.markdown("""
        The Groq API is ready to use. If you see this message, please restart the app.
        """)
        st.stop()
    else:
        # File upload
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.markdown("### Step 1: Choose Your BRD File")
        uploaded_file = st.file_uploader(
            "Drag and drop or click to browse",
            type=['pdf', 'docx', 'txt'],
            help="Upload PDF, DOCX, or TXT format",
            label_visibility="collapsed"
        )
        st.caption("📄 Supported: **PDF** • **DOCX** • **TXT**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                st.session_state.temp_file_path = tmp_file.name
            
            st.success(f"✅ **{uploaded_file.name}** is ready for processing")
            st.markdown("### Step 2: Start AI Processing")
            
            # Process button
            if st.button("🚀 START AI PROCESSING", type="primary", use_container_width=True):
                try:
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
                    status_text.markdown("### 🔍 Stage 1/6: Analyzing BRD Structure...")
                    progress_bar.progress(1/6)
                    st.session_state.current_stage = 1
                    
                    parsing_result = brd_parser.parse_brd(st.session_state.temp_file_path)
                    st.session_state.processed_data['parsing'] = parsing_result
                    
                    # Extract and store BRD text
                    st.session_state.brd_text = brd_parser.extract_text_from_file(st.session_state.temp_file_path)
                    
                    # Stage 2: Requirement Extraction
                    status_text.markdown("### 📋 Stage 2/6: Extracting Requirements...")
                    progress_bar.progress(2/6)
                    st.session_state.current_stage = 2
                    
                    requirements = req_extractor.extract_requirements(
                        st.session_state.brd_text,
                        parsing_result
                    )
                    st.session_state.processed_data['requirements'] = requirements
                    
                    # Stage 3: Context Synthesis
                    status_text.markdown("### 🎯 Stage 3/6: Synthesizing Business Context...")
                    progress_bar.progress(3/6)
                    st.session_state.current_stage = 3
                    
                    context = context_synth.synthesize_context(requirements)
                    st.session_state.processed_data['context'] = context
                    
                    # Stage 4: User Story Generation
                    status_text.markdown("### ✍️ Stage 4/6: Generating User Stories...")
                    progress_bar.progress(4/6)
                    st.session_state.current_stage = 4
                    
                    stories = story_gen.generate_stories(requirements, context)
                    st.session_state.processed_data['stories'] = stories
                    
                    # Stage 5: QA Validation
                    status_text.markdown("### ✔️ Stage 5/6: Validating Quality...")
                    progress_bar.progress(5/6)
                    st.session_state.current_stage = 5
                    
                    validation = qa_validator.validate_stories(requirements, stories)
                    st.session_state.processed_data['validation'] = validation
                    
                    # Stage 6: Output Transformation
                    status_text.markdown("### 📦 Stage 6/6: Preparing Exports...")
                    progress_bar.progress(6/6)
                    st.session_state.current_stage = 6
                    
                    output = output_transformer.transform_for_export(stories, context)
                    st.session_state.processed_data['output'] = output
                    
                    # Complete
                    progress_bar.progress(1.0)
                    status_text.markdown("### ✅ **Processing Complete!**")
                    st.session_state.current_stage = 7
                    
                    st.balloons()
                    st.success("🎉 **Success!** User stories generated. Check the results tab!")
                    
                except Exception as e:
                    st.error(f"❌ **Processing Error:** {str(e)}")
                    with st.expander("View Error Details"):
                        st.code(traceback.format_exc())

with tab2:
    st.header("Processing Results & Analysis")
    
    if not st.session_state.processed_data:
        st.info("👆 **Upload and process a BRD document first**")
        st.markdown("""
         Once complete, you'll see:
        - 📊 **Summary metrics** and quality scores
        - 📌 **Stage-by-stage** analysis results 
        - 📋 **Generated user stories** with traceability
        """)
    else:
        # Summary metrics first
        if 'stories' in st.session_state.processed_data:
            st.subheader("📊 Key Metrics")
            
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
                with st.expander(stage_title, expanded=False):
                    stage_data = st.session_state.processed_data[stage_key]
                    
                    # Show key highlights
                    if stage_key == 'parsing':
                        completeness = stage_data.get('completeness_score', 0)
                        st.markdown(f"**Completeness Score:** {completeness}/100")
                    elif stage_key == 'requirements':
                        fr_count = len(stage_data.get('functional_requirements', []))
                        nfr_count = len(stage_data.get('non_functional_requirements', []))
                        st.markdown(f"**Functional:** {fr_count} | **Non-Functional:** {nfr_count}")
                    elif stage_key == 'context':
                        personas = len(stage_data.get('user_personas', []))
                        st.markdown(f"**User Personas:** {personas}")
                    elif stage_key == 'stories':
                        stories_count = len(stage_data.get('user_stories', []))
                        st.markdown(f"**Total Stories:** {stories_count}")
                    elif stage_key == 'validation':
                        issues = len(stage_data.get('ambiguity_issues', [])) + len(stage_data.get('testability_issues', []))
                        st.markdown(f"**Issues Flagged:** {issues}")
                    
                    st.json(stage_data)

with tab3:
    st.header("Export User Stories")
    
    if 'output' not in st.session_state.processed_data:
        st.info("👆 **Complete processing first**")
        st.markdown("""
        After processing, download in multiple formats:
        - **PDF** – Executive presentation
        - **Excel** – Jira/Azure DevOps import
        - **Word** – Full documentation
        - **TXT** – Plain text
        """)
    else:
        st.success("🎉 **Your user stories are ready to download!**")
        st.markdown("Choose your preferred format:")
        
        export_handler = ExportHandler()
        output_structure = st.session_state.processed_data['output']
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Export grid
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📄 PDF Export")
            st.caption("Executive-ready presentation")
            if st.button("📥 DOWNLOAD PDF", key="pdf_btn", use_container_width=True, type="primary"):
                try:
                    with st.spinner("Generating PDF..."):
                        pdf_path = export_handler.export_to_pdf(output_structure)
                    with open(pdf_path, 'rb') as f:
                        st.download_button(
                            label="⬇️ Click to Download PDF",
                            data=f.read(),
                            file_name=Path(pdf_path).name,
                            mime="application/pdf",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("### 📝 Word Export")
            st.caption("Comprehensive documentation")
            if st.button("📥 DOWNLOAD WORD", key="word_btn", use_container_width=True, type="primary"):
                try:
                    with st.spinner("Generating Word..."):
                        word_path = export_handler.export_to_word(output_structure)
                    with open(word_path, 'rb') as f:
                        st.download_button(
                            label="⬇️ Click to Download Word",
                            data=f.read(),
                            file_name=Path(word_path).name,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with col2:
            st.markdown("### 📊 Excel Export")
            st.caption("Jira/DevOps compatible")
            if st.button("📥 DOWNLOAD EXCEL", key="excel_btn", use_container_width=True, type="primary"):
                try:
                    with st.spinner("Generating Excel..."):
                        excel_path = export_handler.export_to_excel(output_structure)
                    with open(excel_path, 'rb') as f:
                        st.download_button(
                            label="⬇️ Click to Download Excel",
                            data=f.read(),
                            file_name=Path(excel_path).name,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("### 📋 TXT Export")
            st.caption("Plain text format")
            if st.button("📥 DOWNLOAD TXT", key="txt_btn", use_container_width=True, type="primary"):
                try:
                    with st.spinner("Generating TXT..."):
                        txt_path = export_handler.export_to_txt(output_structure)
                    with open(txt_path, 'r', encoding='utf-8') as f:
                        st.download_button(
                            label="⬇️ Click to Download TXT",
                            data=f.read(),
                            file_name=Path(txt_path).name,
                            mime="text/plain",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 2rem 0;">
    <p style="margin: 0; font-size: 1rem; font-weight: 600;">
        <span style="color: #FFD700;">⚡ Embridge</span> Enterprise AI Solutions
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
        Powered by Groq AI ⚡ (Llama 3.3 70B)
    </p>
</div>
""", unsafe_allow_html=True)
