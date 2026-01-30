"""
Quick verification script to test the application setup
"""
import sys
from pathlib import Path

def verify_installation():
    """Verify all components are properly installed"""
    print("🔍 BRD to User Story Generator - Installation Verification\n")
    print("=" * 60)
    
    # Check Python version
    print(f"\n✓ Python Version: {sys.version.split()[0]}")
    
    # Check required modules
    required_modules = [
        'streamlit',
        'openai',
        'dotenv',
        'PyPDF2',
        'docx',
        'openpyxl',
        'reportlab',
        'pandas'
    ]
    
    print("\n📦 Checking Dependencies:")
    missing = []
    for module in required_modules:
        try:
            if module == 'dotenv':
                __import__('dotenv')
            elif module == 'docx':
                __import__('docx')
            else:
                __import__(module.lower())
            print(f"  ✓ {module}")
        except ImportError:
            print(f"  ✗ {module} - MISSING")
            missing.append(module)
    
    # Check project structure
    print("\n📁 Checking Project Structure:")
    base_dir = Path(__file__).parent
    
    required_files = [
        'app.py',
        'config.py',
        'requirements.txt',
        '.env.example',
        'README.md',
        'modules/__init__.py',
        'modules/brd_parser.py',
        'modules/requirement_extractor.py',
        'modules/context_synthesizer.py',
        'modules/story_generator.py',
        'modules/qa_validator.py',
        'modules/output_transformer.py',
        'modules/openai_service.py',
        'modules/export_handlers.py',
        'prompts/task1_brd_parsing.txt',
        'prompts/task2_extraction.txt',
        'prompts/task3_synthesis.txt',
        'prompts/task4_generation.txt',
        'prompts/task5_validation.txt',
        'prompts/task6_transformation.txt'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - MISSING")
            missing_files.append(file_path)
    
    # Check directories
    print("\n📂 Checking Directories:")
    required_dirs = ['exports', 'assets', 'prompts', 'modules']
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ - MISSING")
    
    # Check configuration
    print("\n⚙️  Configuration Status:")
    env_file = base_dir / '.env'
    if env_file.exists():
        print("  ✓ .env file found")
        # Check if configured
        try:
            from config import Config
            if Config.is_configured():
                print("  ✓ Azure OpenAI configured")
            else:
                print("  ⚠ Azure OpenAI NOT configured - needs API credentials")
                missing_vars = Config.validate()
                for var in missing_vars:
                    print(f"    - Missing: {var}")
        except Exception as e:
            print(f"  ✗ Error loading config: {e}")
    else:
        print("  ⚠ .env file not found - copy from .env.example and configure")
    
    # Summary
    print("\n" + "=" * 60)
    print("\n📊 VERIFICATION SUMMARY:")
    
    if missing:
        print(f"\n❌ Missing {len(missing)} dependencies:")
        for m in missing:
            print(f"   - {m}")
        print("\n   Run: pip install -r requirements.txt")
    else:
        print("\n✅ All dependencies installed")
    
    if missing_files:
        print(f"\n❌ Missing {len(missing_files)} files - reinstallation may be needed")
    else:
        print("✅ All required files present")
    
    if not env_file.exists():
        print("\n⚠️  Configuration needed:")
        print("   1. Copy .env.example to .env")
        print("   2. Add Azure OpenAI credentials")
    
    print("\n" + "=" * 60)
    
    if not missing and not missing_files and env_file.exists():
        print("\n🎉 Installation verified! Ready to run:")
        print("   streamlit run app.py")
    else:
        print("\n⚠️  Some issues found - please resolve before running")
    
    print()

if __name__ == "__main__":
    verify_installation()
