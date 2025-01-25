import docx
import PyPDF2
import io

def extract_file_content(file):
    """Extract content from different file types"""
    try:
        # Get file extension
        file_name = file.name.lower()

        # Handle different file types
        if file_name.endswith('.txt'):
            return file.read().decode('utf-8')

        elif file_name.endswith('.docx'):
            doc = docx.Document(file)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

        elif file_name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text

        else:
            return "Unsupported file type. Please upload .txt, .docx, or .pdf files."

    except Exception as e:
        return f"Error extracting file content: {str(e)}"
