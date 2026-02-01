# OCR Support Guide

The BRD to User Story Generator includes **dual OCR support** for processing scanned or image-based PDF documents:

## 🚀 Mistral OCR (Primary - FREE & UNLIMITED)

**Powered by Puter.js**
- ✅ **Completely FREE** with no usage limits
- ✅ **No API keys required**
- ✅ **No installation needed** - works instantly in browser
- ✅ **Multilingual support** - supports multiple languages
- ✅ **Advanced document understanding** - handles complex layouts
- ⚡ **Fast processing** with Mistral AI

### How it Works
Mistral OCR uses the "User-Pays" model through Puter.js, where:
1. The OCR processing happens in the user's browser
2. Puter.js connects to Mistral's OCR service
3. No cost to the developer or user
4. No backend setup required

### Automatic Activation
Mistral OCR automatically activates when:
- A PDF has minimal extractable text (< 100 words)
- Pages appear to be image-based or scanned
- Standard text extraction fails

## 📸 Tesseract OCR (Fallback)

**Local OCR Engine**
- ✅ **Works offline** once installed
- ✅ **Privacy-focused** - all processing local
- ⚠️ **Requires installation** on Windows

### Installation (Windows)

If Mistral OCR fails or you want offline OCR:

1. **Download Tesseract OCR:**
   - Visit: https://github.com/UB-Mannheim/tesseract/wiki
   - Download the Windows installer
   - Run installation (default path: `C:\Program Files\Tesseract-OCR\`)

2. **Verify Installation:**
   - Open Command Prompt
   - Run: `tesseract --version`
   - Should display version information

3. **No Configuration Needed:**
   - The app automatically detects Tesseract in standard locations
   - Both `C:\Program Files\Tesseract-OCR\` and `C:\Program Files (x86)\Tesseract-OCR\` are checked

## 🎯 OCR Processing Flow

```
1. Upload PDF
2. Check if text extractable
3. If YES → Use standard extraction ✅
4. If NO → Try Mistral OCR (free, unlimited) 🚀
5. If Mistral fails → Fallback to Tesseract OCR 📸
6. Extract and process text
```

## 📋 Supported Formats

### Direct Text Extraction (No OCR needed):
- ✅ **Text-based PDFs** - Created from Word, Google Docs, etc.
- ✅ **DOCX files** - Microsoft Word documents
- ✅ **TXT files** - Plain text files

### OCR-Required formats:
- 📸 **Scanned PDFs** - Documents scanned from paper
- 📸 **Image-based PDFs** - PDFs containing images of text
- 📸 **Screenshots** - PDF exports of screenshots

## 💡 Best Practices

### For Best OCR Results:
1. **High Resolution:** Use 300 DPI or higher when scanning
2. **Clear Text:** Ensure text is legible and not blurry
3. **Good Contrast:** Black text on white background works best
4. **Proper Alignment:** Keep documents straight when scanning
5. **Clean Pages:** Remove smudges, coffee stains, or marks

### File Size Optimization:
- Keep PDFs under 10 MB for faster processing
- Use compressed images when possible
- Mistral OCR works best with clear, high-contrast images

## 🛠️ Troubleshooting

### Mistral OCR Not Working?
- Check internet connection (Puter.js requires network)
- Refresh the browser page
- Try uploading again
- Check browser console for errors

### Tesseract OCR Not Working?
- Verify Tesseract is installed: Run `tesseract --version` in Command Prompt
- Check installation path is correct
- Reinstall Tesseract if needed
- Ensure `pytesseract` Python package is installed: `pip install pytesseract`

### Low Quality Results?
- Try re-scanning at higher DPI (300+)
- Improve document contrast before scanning
- Use Tesseract for offline processing if Mistral has issues
- Consider manually typing very poor quality scans

## 🔍 OCR vs. Standard Text

| Feature | Standard Text Extraction | Mistral OCR | Tesseract OCR |
|---------|-------------------------|-------------|---------------|
| Speed | ⚡ Instant | 🚀 Fast | 🐢 Slower |
| Cost | Free | Free (Unlimited) | Free |
| Internet Required | No | Yes | No |
| Installation | None | None | Required |
| Accuracy | Perfect | Excellent | Good |
| Languages | All | Many | Many (with language packs) |

## 📞 Support

For OCR-related issues:
1. Check this guide first
2. Verify your document quality
3. Try both OCR methods
4. Review error messages in the UI
