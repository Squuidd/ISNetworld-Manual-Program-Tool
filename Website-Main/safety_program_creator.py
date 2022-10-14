from venv import create
from docxtpl import DocxTemplate
from docxtpl.subdoc import Subdoc, SubdocComposer
from docx import Document
from zipfile import ZipFile

from lxml import etree  # TODO for debug
import re
import io

import types

import os


# import win32com.client

# import inspect, os

def findPath(file_name):
    script_dir = os.path.dirname(__file__)  # absolute dir the script is in
    rel_path = f"Safety Programs/{file_name}"
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path


# def update_toc(docx_file):
#     word = win32com.client.DispatchEx("Word.Application")
#     doc = word.Documents.Open(docx_file)
#     doc.TablesOfContents(1).Update()
#     doc.Close(SaveChanges=True)
#     word.Quit()

def DocumentBytes(doc):
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream.getvalue()


class DummyDoc(Subdoc):
    def __init__(self, tpl, xml):
        super().__init__(tpl)  # tpl is main document, it is normally passed to subdoc class
        self.xml = xml

    def _get_xml(self):  # Spoof the xml with our own
        return self.xml


def create_manual(
        file,
        safety_documents,
        company_name
):
    main_document = DocxTemplate(file)
    # Create subdoc to insert into main document
    main_document.init_docx()  # Not sure what the point of this is but lib normally does it before init Subdoc.

    xml = ""
    compose = SubdocComposer(main_document)
    for doc in safety_documents:
        sd = Document(doc)
        compose.attach_parts(sd)

        # Remove any sections because it breaks shit
        if sd.element.body.sectPr is not None:
            sd.element.body.remove(sd.element.body.sectPr)

        # add the bodies of every subdoc to our xml
        xml += re.sub(r'</?w:body[^>]*>', '', etree.tostring(
            sd.element.body, encoding='unicode', pretty_print=False))

    subdoc = DummyDoc(main_document, xml)

    ctx = {
        "safety": subdoc,
        "company_name": company_name
    }

    main_document.render(ctx)  # Render

    return DocumentBytes(main_document)

    # updates TOC *windows only*
    # script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    # file_name = save_path
    # file_path = os.path.join(script_dir, file_name)
    # update_toc(file_path)

    # print(etree.tostring(main_document.element.body, encoding='unicode', pretty_print=True))


def create_program(
        files: list,  # TODO Should maybe be bytes
        company_name: str
):
    docs = []
    for file in files:
        main_document = DocxTemplate(file)

        ctx = {
            "company_name": company_name
        }

        main_document.render(ctx)

        docs.append(
            [
                os.path.basename(file),
                DocumentBytes(main_document)
            ]
        )
    return zip_files(docs).getvalue()

def zip_files(files):
    mem_zip = io.BytesIO()
    with ZipFile(mem_zip, mode="w") as zf:
        for file in files:
            zf.writestr(file[0], file[1])
    zf.close()
    return mem_zip

# create_manual(findPath("safety_manual.docx"), [findPath("aerial lifts.docx"), findPath("cranes.docx"), findPath("cadmium.docx")], "Test Name LLC.")
# update_toc('Output/new_safety_manual.docx')

# create_program(findPath("aerial lifts.docx"), "Test Name.")
