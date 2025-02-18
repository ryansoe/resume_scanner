import os
import pdfminer.high_level
import docx

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        text = pdfminer.high_level.extract_text(pdf_path)
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return None

def extract_text(file_path):
    """Determine file type and extract text accordingly."""
    if not os.path.exists(file_path):
        print("File not found!")
        return None

    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        print("Unsupported file type!")
        return None

if __name__ == "__main__":
    # Test the function with sample files
    sample_pdf = "../../data/sample_resume.pdf"
    sample_docx = "../../data/sample_resume.docx"

    print("Extracting PDF Text:\n", extract_text(sample_pdf))
    print("\nExtracting DOCX Text:\n", extract_text(sample_docx))