import glob
import os
from tkinter.ttk import Style
from xml.dom.minidom import Document
from docx.enum.style import WD_STYLE_TYPE
#from docx.enum.table import WD_ALIGN_HORIZONTAL
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

def createStyles(document):
    styles = document.styles

    header_style = styles.add_style("table_header", WD_STYLE_TYPE.PARAGRAPH)
    header_font = header_style.font 
    header_font.name = "Arial"
    header_font.bold = True
    header_font.size = docx.shared.Pt(18)

    manual_title_style = styles.add_style("manual_title", WD_STYLE_TYPE.PARAGRAPH)
    manual_title_font = manual_title_style.font
    manual_title_font.name = "Cambria"
    manual_title_font.bold = True
    manual_title_font.size = docx.shared.Pt(26)

    manual_subtext_style = styles.add_style("manual_subtext", WD_STYLE_TYPE.PARAGRAPH)
    manual_subtext_font = manual_subtext_style.font
    manual_subtext_font.name = "Cambria"
    manual_subtext_font.bold = True
    manual_subtext_font.size = docx.shared.Pt(16)




def addCompanyName(table, doc, style):
    name_row = table.rows[0].cells
    company_name = name_row[0]
    company_name.text = f"{COMPANY_NAME}"
    
    paragraph = company_name.paragraphs[0]
    paragraph.style = doc.styles[style]
    #company_name.vertical_alignment = WD_ALIGN_HORIZONTAL.CENTER

    save_path = f"Output/{chosen_file}"
    doc.save(save_path)
    createPDF(save_path, save_path)


def manualTitle(table, doc, style):
    name_row = table.rows[0].cells
    company_name = name_row[0]
    company_name.text = f"{COMPANY_NAME}\n\n"
    
    paragraph = company_name.paragraphs[0]
    paragraph.style = doc.styles[style]


    subtext = company_name.add_paragraph("Safety, Health, and Environmental Manual")
    subtext.style = doc.styles["manual_subtext"]
    #company_name.vertical_alignment = WD_ALIGN_HORIZONTAL.CENTER

    save_path = f"Output/{chosen_file}"
    doc.save(save_path)
    createPDF(save_path, save_path)    

#TODO add another func like above but that doesnt go in to header.



def createPDF(start_path, save_path):
    size = len(start_path)
    pdf_name = f"{start_path[:size - 5]}.pdf"
    convert(start_path, pdf_name)

def createSafetyProgram(path):
    document = docx.Document(path)
    createStyles(document)

    section = document.sections[0]
    header = section.header
    for table in header.tables:
        addCompanyName(table, document, "table_header")
    

def createSafetyManual(path):
    document = docx.Document(path)
    createStyles(document)

    page_count = len(document.sections)

    for i in range(page_count):
        if i == 0:
            section = document.sections[i]
            manualTitle(document.tables[0], document, "manual_title")
        section = document.sections[i]
        header = section.header
        for table in header.tables:
            addCompanyName(table, document, "table_header")

def replace_string(filename, c_name):
    doc = docx.Document(f"Safety Programs/{filename}")
    title = doc.paragraphs[0]

    title.text = COMPANY_NAME


    print(title.text)
    # for p in doc.paragraphs:
    #     if 'Company Name Here' in p.text:
    #         inline = p.runs
    #         # Loop added to work with runs (strings with same style)
    #         for i in range(len(inline)):
    #             if 'Company Name Here' in inline[i].text:
    #                 text = inline[i].text.replace('Company Name Here', c_name)
    #                 inline[i].text = text
    #         print(p.text)
    doc.save("Output/test.docx")

def createTOC():
    pass

#replace_string(chosen_file, COMPANY_NAME)
# createSafetyProgram(findPath(chosen_file))
createSafetyManual(findPath(chosen_file))