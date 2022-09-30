from docxtpl import DocxTemplate
from docxtpl.subdoc import Subdoc, SubdocComposer
from docx import Document

from lxml import etree
import re

import types

class DummyDoc(Subdoc):
    def __init__(self, tpl, xml):
        super().__init__(tpl)
        self.xml = xml

    def _get_xml(self):
        return self.xml

def main(
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
    main_document.save('demo.docx')

main("safety_manual.docx", ["aerial_lifts.docx", "aerial_lifts.docx"], "Walter White")
