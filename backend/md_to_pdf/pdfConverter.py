from spire.doc import *
from spire.doc.common import *

def MDtoPDF(file_path):
    # Create a Document object
    dokumencik = Document()

    # Load a Markdown file
    dokumencik.LoadFromFile(file_path)

    # Save it as a pdf file
    dokumencik.SaveToFile("backend/md_to_pdf/result.pdf", FileFormat.PDF)
    
    # Dispose resources
    dokumencik.Dispose()

MDtoPDF('backend/md_to_pdf/sprint11.md')