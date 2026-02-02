def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    try:
        import pypdf
    except ImportError:
        raise ImportError("pypdf not installed. Run: pip install pypdf")
    
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = pypdf.PdfReader(file)
        num_pages = len(reader.pages)
        
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            text += f"\n--- Page {i+1} ---\n"
            text += page_text
    
    return text