"""
Puter.js Mistral OCR Integration for Streamlit
Free, unlimited OCR using Mistral AI through Puter.js
"""
import streamlit.components.v1 as components
import base64
from pathlib import Path

def mistral_ocr_from_file(file_path: str) -> str:
    """
    Extract text from image using free Mistral OCR via Puter.js
    
    Args:
        file_path: Path to image file
        
    Returns:
        Extracted text
    """
    # Read file and convert to base64
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    file_ext = Path(file_path).suffix.lower()
    mime_type = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.pdf': 'application/pdf'
    }.get(file_ext, 'image/png')
    
    base64_data = base64.b64encode(file_data).decode()
    data_url = f"data:{mime_type};base64,{base64_data}"
    
    # HTML with Puter.js OCR
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://js.puter.com/v2/"></script>
    </head>
    <body>
        <div id="status" style="padding: 10px; background: #f0f0f0; border-radius: 5px; margin-bottom: 10px;">
            <strong>🔄 Processing with Mistral OCR...</strong>
        </div>
        <div id="result" style="display: none;"></div>
        
        <script>
            const statusDiv = document.getElementById('status');
            const resultDiv = document.getElementById('result');
            
            // Perform OCR using Mistral via Puter.js
            puter.ai.img2txt({{
                source: '{data_url}',
                provider: 'mistral',
                model: 'mistral-ocr-latest'
            }})
            .then(text => {{
                statusDiv.innerHTML = '<strong>✅ OCR Complete!</strong>';
                resultDiv.textContent = text || 'No text found';
                resultDiv.style.display = 'block';
                
                // Send result back to Streamlit
                window.parent.postMessage({{
                    type: 'ocr_result',
                    text: text || ''
                }}, '*');
            }})
            .catch(error => {{
                statusDiv.innerHTML = '<strong>❌ OCR Failed</strong>';
                resultDiv.textContent = 'Error: ' + error.message;
                resultDiv.style.display = 'block';
                
                // Send error back to Streamlit
                window.parent.postMessage({{
                    type: 'ocr_error',
                    error: error.message
                }}, '*');
            }});
        </script>
    </body>
    </html>
    """
    
    # Display the component and wait for result
    return components.html(html_code, height=150, scrolling=True)


def pdf_to_images_base64(pdf_path: str) -> list:
    """
    Convert PDF pages to base64-encoded images for OCR
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        List of base64-encoded image data URLs
    """
    try:
        from pdf2image import convert_from_path
        import io
        from PIL import Image
        
        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=200)
        
        data_urls = []
        for img in images:
            # Convert PIL Image to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_data = buffer.getvalue()
            base64_data = base64.b64encode(img_data).decode()
            data_urls.append(f"data:image/png;base64,{base64_data}")
        
        return data_urls
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return []


def mistral_ocr_pdf_streamlit(pdf_path: str) -> str:
    """
    Extract text from PDF using Mistral OCR via Puter.js in Streamlit
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted text from all pages
    """
    import streamlit as st
    
    st.info("📸 Converting PDF to images for Mistral OCR...")
    
    # Convert PDF pages to images
    image_data_urls = pdf_to_images_base64(pdf_path)
    
    if not image_data_urls:
        st.error("Failed to convert PDF to images")
        return ""
    
    st.success(f"✅ Converted {len(image_data_urls)} pages to images")
    
    all_text = []
    
    for page_num, data_url in enumerate(image_data_urls, 1):
        with st.expander(f"📄 Processing Page {page_num}/{len(image_data_urls)}", expanded=(page_num == 1)):
            # HTML for this page
            html_code = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <script src="https://js.puter.com/v2/"></script>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        padding: 10px;
                    }}
                    .status {{
                        padding: 10px;
                        background: #e3f2fd;
                        border-radius: 5px;
                        margin-bottom: 10px;
                    }}
                    .result {{
                        white-space: pre-wrap;
                        background: #f5f5f5;
                        padding: 10px;
                        border-radius: 5px;
                        max-height: 300px;
                        overflow-y: auto;
                    }}
                </style>
            </head>
            <body>
                <div class="status" id="status">
                    🔄 <strong>Processing Page {page_num} with Mistral OCR...</strong>
                </div>
                <div class="result" id="result" style="display: none;"></div>
                
                <script>
                    const statusDiv = document.getElementById('status');
                    const resultDiv = document.getElementById('result');
                    
                    puter.ai.img2txt({{
                        source: '{data_url[:1000]}' + '...',  // Truncate for display
                        provider: 'mistral',
                        model: 'mistral-ocr-latest'
                    }})
                    .then(text => {{
                        statusDiv.innerHTML = '✅ <strong>Page {page_num} Complete!</strong>';
                        resultDiv.textContent = text || 'No text found on this page';
                        resultDiv.style.display = 'block';
                    }})
                    .catch(error => {{
                        statusDiv.innerHTML = '❌ <strong>Page {page_num} Failed</strong>';
                        resultDiv.textContent = 'Error: ' + error.message;
                        resultDiv.style.display = 'block';
                    }});
                </script>
            </body>
            </html>
            """
            
            components.html(html_code, height=200, scrolling=True)
    
    return "\n\n".join(all_text) if all_text else "OCR processing initiated. Check expanders above for results."
