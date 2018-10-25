import PyPDF2

def get_hsics_from_pdf(file_path):
    pdfFileObj = open(file_path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # printing number of pages in pdf file
    print(pdfReader.numPages)
    # creating a page object
    pageObj = pdfReader.getPage(1)
    # extracting text from page
    print(pageObj.extractText())
    # closing the pdf file object
    pdfFileObj.close()

if __name__=="__main__":
    file_path = r"C:\Users\qfwang\Downloads\B_HSICSe.pdf"
    get_hsics_from_pdf(file_path)