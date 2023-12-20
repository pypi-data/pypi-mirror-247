import pdfriend.classes.wrappers as wrappers


def remove(infile: str, page_num: int, outfile: str):
    pdf = wrappers.PDFWrapper.Read(infile)

    pdf.pop_page(page_num)

    pdf.write(outfile)
