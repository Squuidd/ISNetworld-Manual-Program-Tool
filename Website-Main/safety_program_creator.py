import glob
import os
from tkinter.ttk import Style
from xml.dom.minidom import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_ALIGN_VERTICAL
import docx

COMPANY_NAME = input("Company name: \n")
chosen_file = input("Choose file: \n")
# chosen_file = "abrasive blasting.docx"

script_dir = os.path.dirname(__file__) # absolute dir the script is in
rel_path = f"Safety Programs/{chosen_file}"
abs_file_path = os.path.join(script_dir, rel_path)

def getText(filename): # use abs_file_path for filenames
    doc = docx.Document(filename)
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


def companyStyle():
    styles = document.styles
    style = styles.add_style("Company", WD_STYLE_TYPE.PARAGRAPH)
    
    font = style.font 
    font.name = "Arial"
    font.bold = True
    font.size = docx.shared.Pt(18)

def addCompanyName(table):
    companyStyle()

    name_row = table.rows[0].cells
    company_name = name_row[0]
    company_name.text = COMPANY_NAME
    
    paragraph = company_name.paragraphs[0]
    paragraph.style = document.styles["Company"]
    company_name.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    document.save(f"Output/{chosen_file}")

document = docx.Document(abs_file_path)
section = document.sections[0]
header = section.header


for table in header.tables:
    addCompanyName(table)

