import aiofiles
import urllib
import mistune
import time
import os

async def write_to_file(filename: str, text: str) -> None:
    """Asynchronously write text to a file in UTF-8 encoding.

    Args:
        filename (str): The filename to write to.
        text (str): The text to write.
    """
    # Ensure text is a string
    if not isinstance(text, str):
        text = str(text)

    # Convert text to UTF-8, replacing any problematic characters
    text_utf8 = text.encode('utf-8', errors='replace').decode('utf-8')

    async with aiofiles.open(filename, "w", encoding='utf-8') as file:
        await file.write(text_utf8)

async def write_text_to_md(text: str, filename: str = "") -> str:
    """Writes text to a Markdown file and returns the file path.

    Args:
        text (str): Text to write to the Markdown file.

    Returns:
        str: The file path of the generated Markdown file.
    """
    file_path = f"outputs/{filename[:60]}.md"
    await write_to_file(file_path, text)
    return urllib.parse.quote(file_path)

async def write_md_to_pdf(text: str, filename: str = "") -> str:
    """Converts Markdown text to a PDF file and returns the file path.

    Args:
        text (str): Markdown text to convert.

    Returns:
        str: The encoded file path of the generated PDF.
    """
    file_path = f"outputs/{filename[:60]}.pdf"

    try:
        from md2pdf.core import md2pdf
        md2pdf(file_path,
               md_content=text,
               # md_file_path=f"{file_path}.md",
               css_file_path="./frontend/pdf_styles.css",
               base_url=None)
        print(f"Report written to {file_path}")
    except Exception as e:
        print(f"Error in converting Markdown to PDF: {e}")
        return ""

    encoded_file_path = urllib.parse.quote(file_path)
    return encoded_file_path

async def write_md_to_word(text: str, filename: str = "") -> str:
    """Converts Markdown text to a DOCX file and returns the file path.

    Args:
        text (str): Markdown text to convert.

    Returns:
        str: The encoded file path of the generated DOCX.
    """
    file_path = f"outputs/{filename[:60]}.docx"

    try:
        from docx import Document
        from htmldocx import HtmlToDocx
        # Convert report markdown to HTML
        html = mistune.html(text)
        # Create a document object
        doc = Document()
        # Convert the html generated from the report to document format
        HtmlToDocx().add_html_to_document(html, doc)

        # Saving the docx document to file_path
        doc.save(file_path)

        print(f"Report written to {file_path}")

        encoded_file_path = urllib.parse.quote(file_path)
        return encoded_file_path

    except Exception as e:
        print(f"Error in converting Markdown to DOCX: {e}")
        return ""
    
async def export_pdf(text: str) -> bytes:
    """Converts Markdown text to a PDF file and returns the file buffer.

    Args:
        text (str): Markdown text to convert.

    Returns:
        bytes: The PDF file contents as bytes.
    """
    temp_path = f"outputs/temp_{int(time.time())}.pdf"
    
    try:
        from md2pdf.core import md2pdf
        md2pdf(temp_path,
            md_content=text,
            css_file_path="./frontend/pdf_styles.css",
            base_url=None)
        
        # Read file into buffer
        with open(temp_path, 'rb') as f:
            file_buffer = f.read()
            
        # Delete temp file
        os.remove(temp_path)
        
        return file_buffer
    except Exception as e:
        print(f"Error in generating PDF: {e}")
        return ""


async def export_docx(text: str) -> bytes:
    """Converts Markdown text to a DOCX file and returns the file buffer.

    Args:
        text (str): Markdown text to convert.

    Returns:
        bytes: The DOCX file contents as bytes.
    """
    temp_path = f"outputs/temp_{int(time.time())}.docx"
    
    try:
        from docx import Document
        from htmldocx import HtmlToDocx
        
        # Convert report markdown to HTML
        html = mistune.html(text)
        
        # Create a document object
        doc = Document()
    
        # Convert the html generated from the report to document format
        HtmlToDocx().add_html_to_document(html, doc)
        
        # Save the document to the temporary file
        doc.save(temp_path)

        
        # Read the document into a buffer
        with open(temp_path, 'rb') as f:
            file_buffer = f.read()
            
        # Delete temp file
        os.remove(temp_path)
        
        return file_buffer  
    except Exception as e:
        print(f"Error in generating DOCX: {e}")
        return ""
