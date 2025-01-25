from spire.pdf import *
from spire.pdf.common import *

def MDtoPDF(file_path):
    # Create a Document object
    document = Document()

    # Load a Markdown file
    document.LoadFromFile(file_path)

    # Save it as a pdf file
    document.SaveToFile("backend/mDtoPDF/ToPdf.pdf", FileFormat.PDF)
    
    # Dispose resources
    document.Dispose()

#na pdf jest jakis watermark zjebany, ale mozna go olac bo komu sie chce licencje kupować, jako noralni pracownicy oczysicie uzylibysmy licencjonowaneg ooprogramowania ;333
MDtoPDF('backend/mDtoPDF/markdown-sample.md')