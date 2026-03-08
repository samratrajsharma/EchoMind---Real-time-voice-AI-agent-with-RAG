import os
from pypdf import PdfReader
import docx


def load_document(file_path: str) -> str:
    """
    Detect file type and extract text.
    """

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return load_pdf(file_path)

    elif extension == ".docx":
        return load_docx(file_path)

    elif extension in [".txt", ".md"]:
        return load_text(file_path)

    else:
        raise ValueError(f"Unsupported file type: {extension}")


def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text


def load_docx(file_path: str) -> str:
    doc = docx.Document(file_path)

    text = ""

    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text


def load_text(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()