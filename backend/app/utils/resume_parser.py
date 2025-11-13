import PyPDF2
import docx
import io
import asyncio

async def extract_text_from_pdf(file_content: bytes) -> str:
    try:
        return await asyncio.to_thread(_parse_pdf, file_content)
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")

def _parse_pdf(file_content: bytes) -> str:
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
    text = ""
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text.strip()

async def extract_text_from_docx(file_content: bytes) -> str:
    try:
        return await asyncio.to_thread(_parse_docx, file_content)
    except Exception as e:
        raise ValueError(f"Failed to parse DOCX: {str(e)}")

def _parse_docx(file_content: bytes) -> str:
    doc = docx.Document(io.BytesIO(file_content))
    return "\n".join([para.text for para in doc.paragraphs]).strip()

async def extract_text_from_txt(file_content: bytes) -> str:
    try:
        return await asyncio.to_thread(lambda: file_content.decode('utf-8').strip())
    except Exception as e:
        raise ValueError(f"Failed to parse TXT: {str(e)}")

async def parse_resume(file_content: bytes, filename: str) -> str:
    filename_lower = filename.lower()

    if filename_lower.endswith('.pdf'):
        return await extract_text_from_pdf(file_content)
    elif filename_lower.endswith('.docx') or filename_lower.endswith('.doc'):
        return await extract_text_from_docx(file_content)
    elif filename_lower.endswith('.txt'):
        return await extract_text_from_txt(file_content)
    else:
        raise ValueError("Unsupported file format. Please upload PDF, DOCX, or TXT")
