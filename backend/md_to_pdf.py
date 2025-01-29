from spire.doc import *
from spire.doc.common import *

def convert(md_path, output_file):
    # Create a Document object
    dokumencik = Document()

    # Load a Markdown file
    dokumencik.LoadFromFile(md_path)

    # Save it as a pdf file
    dokumencik.SaveToFile(output_file, FileFormat.PDF)
    
    # Dispose resources
    dokumencik.Dispose()
#convert("outputs/merged_output.md", "outputs/raport.pdf")