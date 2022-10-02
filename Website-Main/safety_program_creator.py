from venv import create
from docxtpl import DocxTemplate
from docxtpl.subdoc import Subdoc, SubdocComposer
from docx import Document

from lxml import etree
import re

import types

import os

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

    main_document.save('Output/new_safety_manual.docx')
    print(etree.tostring(main_document.element.body, encoding='unicode', pretty_print=True))

def create_program(
        file, 
        company_name
):
    main_document = DocxTemplate(file)

    ctx = {
        "company_name": company_name
    }

    main_document.render(ctx)

    main_document.save('Output/new_program.docx')
    pass

#create_manual(findPath("safety_manual.docx"), [findPath("aerial lifts.docx"), findPath("cranes.docx"), findPath("cadmium.docx")], "Test Name LLC.")

create_program(findPath("cranes.docx"), "Test Name LLC.")


