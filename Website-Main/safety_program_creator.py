from venv import create
from docxtpl import DocxTemplate
from docxtpl.subdoc import Subdoc, SubdocComposer
from docx import Document

from lxml import etree
import re

import types

import os

import win32com.client

import inspect, os

class DummyDoc(Subdoc):
    def __init__(self, tpl, xml):
        super().__init__(tpl)
        self.xml = xml

    def _get_xml(self):
        return self.xml

def findPath(file_name):
    script_dir = os.path.dirname(__file__) # absolute dir the script is in
    rel_path = f"Safety Programs/{file_name}"
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path

def update_toc(docx_file):
    word = win32com.client.DispatchEx("Word.Application")
    doc = word.Documents.Open(docx_file)
    doc.TablesOfContents(1).Update()
    doc.Close(SaveChanges=True)
    word.Quit()

def create_manual(
        file,
        safety_documents,
        company_name
):
   
    main_document = DocxTemplate(file)
    # Create subdoc to insert into main document
    main_document.init_docx() # Not sure what the point of this is but lib normally does it before init Subdoc.

    xml = ""
    compose = SubdocComposer(main_document)
    for doc in safety_documents:
        sd = Document(doc)
        compose.attach_parts(sd)

        if sd.element.body.sectPr is not None:
            sd.element.body.remove(sd.element.body.sectPr)
        xml += re.sub(r'</?w:body[^>]*>', '', etree.tostring(
            sd.element.body, encoding='unicode', pretty_print=False))

    subdoc = DummyDoc(main_document, xml)

    ctx = {
        "safety": subdoc,
        "company_name": company_name
    }

    main_document.render(ctx)

    save_path = 'Output/new_safety_manual.docx'

    main_document.save(save_path)
    

    # updates TOC *windows only*
    # script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    # file_name = save_path
    # file_path = os.path.join(script_dir, file_name)
    # update_toc(file_path)

    print(etree.tostring(main_document.element.body, encoding='unicode', pretty_print=True))

def create_program(
        files:list, 
        company_name:str
):  

    paths = []

    for file in files:
        main_document = DocxTemplate(file)

        ctx = {
            "company_name": company_name
        }

        main_document.render(ctx)

        filename = os.path.basename(file)

        save_path = f'Output/Programs/{filename}'
        paths.append(save_path)
        main_document.save(save_path)

    return paths
       

#create_manual(findPath("safety_manual.docx"), [findPath("aerial lifts.docx"), findPath("cranes.docx"), findPath("cadmium.docx")], "Test Name LLC.")
#update_toc('Output/new_safety_manual.docx')

#create_program(findPath("aerial lifts.docx"), "Test Name.")


