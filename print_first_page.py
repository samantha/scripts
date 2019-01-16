#!/usr/bin/python3

##
# @file
# @brief   Prints the first page of multiple PDF files to PDF

import PyPDF2, os

your_target_folder = r""

pdf_files = []

for dirpath, _, file_names in os.walk(your_target_folder):

    for files in file_names:
        file_full_path = os.path.abspath(os.path.join(dirpath, files))
        if file_full_path.lower().endswith(".pdf"):
            pdf_files.append(file_full_path)
        else:
            pass

pdf_files.sort(key=str.lower)
pdf_writer = PyPDF2.PdfFileWriter()

for files_address in pdf_files:
    pdf_file_object = open(files_address, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_object)

    page_object = pdf_reader.getPage(0)
    pdf_writer.addPage(page_object)

with open("first_pages.pdf", "wb") as output:
    pdf_writer.write(output)

infile = PyPDF2.PdfFileReader(open('first_pages.pdf', 'rb'))

for i in range(infile.getNumPages()):
    p = infile.getPage(i)
    outfile = PyPDF2.PdfFileWriter()
    outfile.addPage(p)
    with open('file-%02d.pdf' % (i), 'wb') as f:
        outfile.write(f)
