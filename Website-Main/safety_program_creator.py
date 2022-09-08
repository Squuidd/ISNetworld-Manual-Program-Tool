import glob
import os
from tkinter.ttk import Style
from xml.dom.minidom import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_ALIGN_VERTICAL
import docx
from docx2pdf import convert

COMPANY_NAME = input("Company name: \n")
chosen_file = input("Choose file: \n")
# chosen_file = "abrasive blasting.docx"

def findPath(file_name):
    script_dir = os.path.dirname(__file__) # absolute dir the script is in
    rel_path = f"Safety Programs/{file_name}"
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path

def getText(path): # use abs_file_path for filenames
    doc = docx.Document(path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def parseTable(table):
    data = []

    keys = None
    for i, row in enumerate(table.rows):
        text = (cell.text for cell in row.cells)

        # Establish the mapping based on the first row
        # headers; these will become the keys of our dictionary
        if i == 0:
            keys = tuple(text)
            continue

        # Construct a dictionary for this row, mapping
        # keys to values for this row
        row_data = dict(zip(keys, text))

        data.append(row_data)

        return data

def companyStyle(document):
    styles = document.styles
    style = styles.add_style("Company", WD_STYLE_TYPE.PARAGRAPH)
    
    font = style.font 
    font.name = "Arial"
    font.bold = True
    font.size = docx.shared.Pt(18)

def addCompanyName(table, doc):
    companyStyle(doc)

    name_row = table.rows[0].cells
    company_name = name_row[0]
    company_name.text = COMPANY_NAME
    
    paragraph = company_name.paragraphs[0]
    paragraph.style = doc.styles["Company"]
    company_name.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    save_path = f"Output/{chosen_file}"
    doc.save(save_path)
    createPDF(save_path, save_path)

def createPDF(start_path, save_path):
    size = len(start_path)
    pdf_name = f"{start_path[:size - 5]}.pdf"
    convert(start_path, pdf_name)


def createSafetyProgram(path):
    document = docx.Document(path)
    section = document.sections[0]
    header = section.header

    for table in header.tables:
        addCompanyName(table, document)

createSafetyProgram(findPath(chosen_file))