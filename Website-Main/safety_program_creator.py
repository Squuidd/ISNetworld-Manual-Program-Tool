import glob
import os
from xml.dom.minidom import Document
import docx

# chosen_file = input("Choose file: \n")
chosen_file = "abrasive blasting.docx"

script_dir = os.path.dirname(__file__) # absolute dir the script is in
rel_path = f"Safety Programs/{chosen_file}"
abs_file_path = os.path.join(script_dir, rel_path)

def getText(filename): # use abs_file_path for filenames
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

# def printTables(doc):
#     for table in doc.tables:
#         for row in table.rows:
#             for cell in row.cells:
#                 for paragraph in cell.paragraphs:
#                     print(paragraph.text)
#                 printTables(cell)

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

document = docx.Document(abs_file_path)
section = document.sections[0]
header = section.header

for table in header.tables:
    print(parseTable(table))

