import pdf2docx
from docx import Document as Docs
from typing import List, Tuple


def pdf_to_docx(pdf_file: str, docx_file: str) -> None:
    """
    Convert a PDF file to a DOCX file.

    Parameters:
    - pdf_file (str): The path to the input PDF file.
    - docx_file (str): The path to the output DOCX file.
    """
    pdf2docx.parse(pdf_file, docx_file)


def read_document_paragraphs(filename: str) -> List[str]:
    """
    Read paragraphs from a document (DOCX file).

    Parameters:
    - filename (str): The path to the DOCX file.

    Returns:
    List[str]: A list of paragraphs.
    """
    document = Docs(filename)
    paragraphs: List[str] = []
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text)
    return paragraphs


def get_chunks(paragraphs: List[str], chunk_size: int = 10, overlap_size: int = 2) -> List[str]:
    """
    Divide a list of paragraphs into chunks.

    Parameters:
    - paragraphs (List[str]): The list of paragraphs.
    - chunk_size (int): The size of each chunk (default is 10).
    - overlap_size (int): The size of overlap between chunks (default is 2).

    Returns:
    List[str]: A list of chunked paragraphs.
    """
    chunked_paragraphs: List[str] = []

    start_idx = 0
    while start_idx + chunk_size <= len(paragraphs):
        end_idx = start_idx + chunk_size
        chunk = " ".join(paragraphs[start_idx:end_idx])
        chunked_paragraphs.append(chunk)
        start_idx += chunk_size - overlap_size

    else:
        chunk = " ".join(paragraphs[start_idx:])
        chunked_paragraphs.append(chunk)

    return chunked_paragraphs


def extract_text_from_pdf(pdf_path: str, docx_path: str = "converted_document.docx") -> Tuple[str, List[str]]:
    """
    Extract text and paragraphs from a PDF file.

    Parameters:
    - pdf_path (str): The path to the input PDF file.
    - docx_path (str): The path to the output DOCX file (default is "converted_document.docx").

    Returns:
    Tuple[str, List[str]]: A tuple containing the extracted text and a list of paragraphs.
    """
    pdf_to_docx(pdf_path, docx_path)
    paragraphs = read_document_paragraphs(docx_path)
    pdf_text = " ".join(paragraphs)

    return pdf_text, paragraphs


if __name__ == "__main__":
    pdf_path = r"C:\Users\willi\OneDrive\Documents\Internship\WEC AI\model2\pinecone_model\sundar_pichai.pdf"

    print(extract_text_from_pdf(pdf_path=pdf_path))
    print("-" * 10)
    print(get_chunks(paragraphs=[]))  # You need to pass the paragraphs list to the function.
